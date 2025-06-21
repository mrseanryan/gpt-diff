from cornsnake import util_print, util_file
from pathlib import Path

from gpt_diff import config, llm_caller

def run_with_a_diff_file(
    diff_file: Path, target_language: str, config: config.Config
) -> None:
    util_print.print_section("Reading Single 'diff' file")
    diff_file_content = util_file.read_text_from_file(str(diff_file))

    util_print.print_section("Calling Local LLM")
    result_str = llm_caller.call_llm(before_file=diff_file_content, after_file="", config=config)
    # TODO target_language
    # TODO save output


def run_with_a_before_and_after_file(
    path_to_before_file: Path,
    path_to_after_file: Path,
    target_language: str,
    config: config.Config
) -> None:
    util_print.print_section("Reading Before/After Files")
    before_file_content = util_file.read_text_from_file(str(path_to_before_file))
    after_file_content = util_file.read_text_from_file(str(path_to_after_file))

    util_print.print_section("Calling Local LLM")
    result_str = llm_caller.call_llm(before_file=before_file_content, after_file=after_file_content, config=config)
    # TODO target_language
    # TODO save output
