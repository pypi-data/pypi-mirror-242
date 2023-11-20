import argparse
import os
import pathlib
import textwrap
from PIL import Image, UnidentifiedImageError
import re
import requests
import sys
from importlib.metadata import version

from rclip.const import IS_LINUX, IS_MACOS, IS_WINDOWS


MAX_DOWNLOAD_SIZE_BYTES = 50_000_000
DOWNLOAD_TIMEOUT_SECONDS = 60
WIN_ABSOLUTE_FILE_PATH_REGEX = re.compile(r'^[a-z]:\\', re.I)


def __get_system_datadir() -> pathlib.Path:
  '''
  Returns a parent directory path
  where persistent application data can be stored.

  - linux: ~/.local/share
  - macOS: ~/Library/Application Support
  - windows: C:/Users/<USER>/AppData/Roaming
  '''

  home = pathlib.Path.home()

  if IS_WINDOWS:
    return home / 'AppData/Roaming'
  elif IS_LINUX:
    return home / '.local/share'
  elif IS_MACOS:
    return home / 'Library/Application Support'

  raise NotImplementedError(f'"{sys.platform}" is not supported')


def get_app_datadir() -> pathlib.Path:
  app_datadir = os.getenv('RCLIP_DATADIR')
  if app_datadir:
    app_datadir = pathlib.Path(app_datadir)
  else:
    app_datadir = __get_system_datadir() / 'rclip'
  os.makedirs(app_datadir, exist_ok=True)
  return app_datadir


def positive_int_arg_type(arg: str) -> int:
  arg_int = int(arg)
  if arg_int < 1:
    raise argparse.ArgumentTypeError('should be >0')
  return arg_int


def get_terminal_text_width() -> int:
  try:
    return min(100, os.get_terminal_size().columns - 2)
  except OSError:
    return 100


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
  def __init__(self, prog: str, indent_increment: int = 2, max_help_position: int = 24) -> None:
    text_width = get_terminal_text_width()
    super().__init__(prog, indent_increment, max_help_position, width=text_width)


def init_arg_parser() -> argparse.ArgumentParser:
  text_width = get_terminal_text_width()
  parser = argparse.ArgumentParser(
    formatter_class=HelpFormatter,
    prefix_chars='-+',
    description='rclip is an AI-powered command-line photo search tool',
    epilog='hints:\n' +
    textwrap.fill(
      '- relative file path should be prefixed with ./, e.g. "./cat.jpg", not "cat.jpg"',
      initial_indent='  ',
      subsequent_indent='    ',
      width=text_width,
    ) +
    '\n' +
    textwrap.fill(
      '- any query can be prefixed with a multiplier, e.g. "2:cat", "0.5:./cat-sleeps-on-a-chair.jpg";'
      ' adding a multiplier is especially useful when combining image and text queries because'
      ' image queries are usually weighted more than text ones',
      initial_indent='  ',
      subsequent_indent='    ',
      width=text_width,
    ) +
    '\n\n'
    'get help:\n'
    '  https://github.com/yurijmikhalevich/rclip/discussions/new/choose\n\n',
  )
  version_str = f'rclip {version("rclip")}'
  parser.add_argument('--version', '-v', action='version', version=version_str, help=f'prints "{version_str}"')
  parser.add_argument('query', help='a text query or a path/URL to an image file')
  parser.add_argument('--add', '-a', '+', metavar='QUERY', action='append', default=[],
                      help='a text query or a path/URL to an image file to add to the "original" query,'
                      ' can be used multiple times')
  parser.add_argument('--subtract', '--sub', '-s', '-', metavar='QUERY', action='append', default=[],
                      help='a text query or a path/URL to an image file to add to the "original" query,'
                      ' can be used multiple times')
  parser.add_argument('--top', '-t', type=positive_int_arg_type, default=10,
                      help='number of top results to display; default: 10')
  display_mode_group = parser.add_mutually_exclusive_group()
  display_mode_group.add_argument(
    '--preview', '-p',
    action='store_true',
    default=False,
    help='preview results in the terminal (supported in iTerm2, Konsole 22.04+, wezterm, Mintty, mlterm)',
  )
  display_mode_group.add_argument(
    '--filepath-only', '-f', action='store_true', default=False, help='outputs only filepaths',
  )
  parser.add_argument(
    '--preview-height', '-H', metavar='PREVIEW_HEIGHT_PX',
    action='store',
    type=int,
    default=400,
    help='preview height in pixels; default: 400',
  )
  parser.add_argument(
    '--no-indexing', '--skip-index', '--skip-indexing', '-n',
    action='store_true',
    default=False,
    help='allows to skip updating the index if no images were added, changed, or removed'
  )
  parser.add_argument(
    '--indexing-batch-size', '-b', type=positive_int_arg_type, default=8,
    help='the size of the image batch used when updating the search index;'
    ' larger values may improve the indexing speed a bit on some hardware but will increase RAM usage; default: 8',
  )
  parser.add_argument(
    '--exclude-dir',
    action='append',
    help='dir to exclude from search, can be used multiple times;'
    ' adding this argument overrides the default of ("@eaDir", "node_modules", ".git");'
    ' WARNING: the default will be removed in v2'
  )
  if IS_MACOS:
    import torch.backends.mps
    if torch.backends.mps.is_available():
      parser.add_argument('--device', '-d', default='mps', choices=['cpu', 'mps'],
                          help='device to run on; default: mps')
  return parser


def remove_prefix(string: str, prefix: str) -> str:
  '''
  Removes prefix from a string (if present) and returns a new string without a prefix
  TODO(yurij): replace with str.removeprefix once updated to Python 3.9+
  '''
  return string[len(prefix):] if string.startswith(prefix) else string


# See: https://meta.wikimedia.org/wiki/User-Agent_policy
def download_image(url: str) -> Image.Image:
  headers = {'User-agent': 'rclip - (https://github.com/yurijmikhalevich/rclip)'}
  check_size = requests.request('HEAD', url, headers=headers, timeout=60)
  if length := check_size.headers.get('Content-Length'):
      if int(length) > MAX_DOWNLOAD_SIZE_BYTES:
          raise ValueError(f"Avoiding download of large ({length} byte) file.")
  img = Image.open(requests.get(url, headers=headers, stream=True, timeout=DOWNLOAD_TIMEOUT_SECONDS).raw)
  return img


def read_image(query: str) -> Image.Image:
  path = remove_prefix(query, 'file://')
  try:
    img = Image.open(path)
  except UnidentifiedImageError as e:
    # by default the filename on the UnidentifiedImageError is None
    e.filename = path
    raise e
  return img


def is_http_url(path: str) -> bool:
  return path.startswith('https://') or path.startswith('http://')


def is_file_path(path: str) -> bool:
  return (
    path.startswith('/') or
    path.startswith('file://') or
    path.startswith('./') or
    WIN_ABSOLUTE_FILE_PATH_REGEX.match(path) is not None
  )
