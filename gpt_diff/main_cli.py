"""
main.py

Summarize differences between files or a git diff via an LLM.
"""

from pathlib import Path
import sys
from cornsnake import util_print
from optparse import OptionParser

from gpt_diff import process
from gpt_diff.config import read_config


# usage() - prints out the usage text, from the top of this file :-) and the options
def usage(parser: OptionParser) -> None:
    print(__doc__)
    parser.print_help()


# optparse - parse the args
parser = OptionParser(
    usage="%prog <before-file> [after-file] [options]", version="0.1.0"
)

parser.add_option(
    "-l",
    "--language",
    dest="target_language",
    metavar="TARGET_LANGUAGE",  # 'metavar' helps make 'help' messages refer to values and is used to build the help for this option.
    default="English",
    help="translate to the target output language TARGET_LANGUAGE. Example: English.",
)
parser.add_option(
    "-o",
    "--output",
    dest="output_dir",
    default=None,
    help="the output directory. By default is None, so output is to stdout (no files are output).",
)
parser.add_option(
    "-v",
    "--verbose",
    action="store_true",
    help="turn on verbose mode",
    dest="is_verbose",
)


def process_args() -> None:
    (options, args) = parser.parse_args()

    target_language = options.target_language

    config = read_config()
    
    config.is_verbose = options.is_verbose

    try:
        match len(args):
            case 1:
                path_to_before_file = args[0]
                process.run_with_a_diff_file(
                    diff_file=Path(path_to_before_file),
                    target_language=target_language,
                    config=config,
                )
            case 2:
                path_to_before_file = args[0]
                path_to_after_file = args[1]
                process.run_with_a_before_and_after_file(
                    path_to_before_file=Path(path_to_before_file),
                    path_to_after_file=Path(path_to_after_file),
                    target_language=target_language,
                    config=config,
                )
            case _:
                usage(parser)
                sys.exit(2)
    except Exception as e:
        util_print.print_error(f"An error occurred: {str(e)}")
        sys.exit(3)


if __name__ == "__main__":
    process_args()
