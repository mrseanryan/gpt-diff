from cornsnake import util_print, util_file
from pathlib import Path

from gpt_diff import config, llm_caller

def _read_input_file(path_to_file: Path) -> str:
    util_print.print_custom(f"Reading file {path_to_file}")
    return util_file.read_text_from_file(str(path_to_file))


def _write_output_to_file(result_str: str, output_file: Path) -> None:
    util_print.print_result(f"Writing output to {output_file}")
    util_file.write_text_to_file(text=result_str, filepath=str(output_file))


def run_with_a_diff_file(
    diff_file: Path, target_language: str, config: config.Config, output_file: Path
) -> None:
    util_print.print_section("Reading Single 'diff' file")
    diff_file_content = _read_input_file(path_to_file=diff_file)

    util_print.print_section("Calling Local LLM")
    result_str = llm_caller.call_llm(
        before_file=diff_file_content,
        after_file="",
        config=config,
        target_language=target_language,
    )
    _write_output_to_file(result_str=result_str, output_file=output_file)


def run_with_a_before_and_after_file(
    path_to_before_file: Path,
    path_to_after_file: Path,
    target_language: str,
    config: config.Config,
    output_file: Path,
) -> None:
    util_print.print_section("Reading Before/After Files")
    before_file_content = _read_input_file(path_to_file=path_to_before_file)
    after_file_content = _read_input_file(path_to_file=path_to_after_file)

    util_print.print_section("Calling Local LLM")
    result_str = llm_caller.call_llm(
        before_file=before_file_content,
        after_file=after_file_content,
        config=config,
        target_language=target_language,
    )
    _write_output_to_file(result_str=result_str, output_file=output_file)
