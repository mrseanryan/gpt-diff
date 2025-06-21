"""
main.py

Summarize differences between files or a git diff via an LLM.
"""

from pathlib import Path
import sys
from cornsnake import util_pdf, util_print
from optparse import OptionParser, Values

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
parser.add_option("-e", "--end-page", dest="end_page", type="int", default=-1,
                    help="(for PDF file) The End page (1-indexed) to extract text to.")
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
    dest="output_file",
    default=None,
    help="the output file. By default is None, so output is to stdout (no file is output).",
)
parser.add_option("-s", "--start-page", dest="start_page", type="int", default=-1,
                    help="(for PDF files) The Start page (1-indexed) to extract text from.")
parser.add_option(
    "-v",
    "--verbose",
    action="store_true",
    help="turn on verbose mode",
    dest="is_verbose",
)

def _are_pdf_options_set(options: Values, parser: OptionParser) -> bool:
    return options.start_page != -1 or options.end_page != -1

def _raise_start_end_options_not_relevant(parser: OptionParser) -> None:
    parser.error("The options start_page and end_page are only relevant when comparing 2 PDF files.")

def process_args() -> None:
    (options, args) = parser.parse_args()

    config = read_config()

    config.is_verbose = options.is_verbose

    try:
        match len(args):
            case 1:
                if _are_pdf_options_set(parser=parser, options=options):
                    _raise_start_end_options_not_relevant(parser=parser)
                    sys.exit(2)

                path_to_before_file = args[0]
                process.run_with_a_diff_file(
                    diff_file=Path(path_to_before_file),
                    target_language=options.target_language,
                    config=config,
                    output_file=Path(options.output_file),
                )
            case 2:
                path_to_before_file = args[0]
                path_to_after_file = args[1]

                are_both_pdf = util_pdf.is_pdf(filepath=path_to_before_file) and util_pdf.is_pdf(filepath=path_to_after_file)
                if not(are_both_pdf) and _are_pdf_options_set(parser=parser, options=options):
                    _raise_start_end_options_not_relevant(parser=parser)
                    sys.exit(2)

                process.run_with_a_before_and_after_file(
                    path_to_before_file=Path(path_to_before_file),
                    path_to_after_file=Path(path_to_after_file),
                    target_language=options.target_language,
                    config=config,
                    output_file=Path(options.output_file),
                    start_page=options.start_page,
                    end_page=options.end_page
                )
            case _:
                usage(parser)
                sys.exit(3)
    except Exception as e:
        util_print.print_error(f"An error occurred: {str(e)}")
        sys.exit(4)


if __name__ == "__main__":
    process_args()
