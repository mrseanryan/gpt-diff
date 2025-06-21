import typing
from cornsnake import util_pdf, util_print, util_file, util_time
from pathlib import Path

from gpt_diff import config, llm_caller


def _read_pdf_input_file(path_to_file: Path, start_page: int, end_page: int) -> str:
    result: str = typing.cast(
        str,
        util_pdf.extract_text_from_pdf(
            filepath=str(path_to_file), start_page=start_page, end_page=end_page
        ),
    )
    return result


def _read_input_file(
    path_to_file: Path, start_page: int = -1, end_page: int = -1
) -> str:
    util_print.print_custom(f"Reading file {path_to_file}")
    if util_pdf.is_pdf(filepath=str(path_to_file)):
        return _read_pdf_input_file(
            path_to_file=path_to_file, start_page=start_page, end_page=end_page
        )
    return typing.cast(str, util_file.read_text_from_file(str(path_to_file)))


def _write_output_to_file(result_str: str, output_file: Path) -> None:
    util_print.print_result(f"Writing output to {output_file}")
    util_file.write_text_to_file(text=result_str, filepath=str(output_file))


def _summarize_differences(
    before_file_content: str,
    after_file_content: str,
    config: config.Config,
    target_language: str,
    output_file: Path,
    extra_user_prompt: str,
) -> None:
    start = util_time.start_timer()
    util_print.print_section("Calling Local LLM")
    result_str = llm_caller.call_llm(
        before_file=before_file_content,
        after_file=after_file_content,
        config=config,
        target_language=target_language,
        extra_user_prompt=extra_user_prompt,
    )
    _write_output_to_file(result_str=result_str, output_file=output_file)

    elapsed_seconds = util_time.end_timer(start)
    util_print.print_result(
        f"Processed in {util_time.describe_elapsed_seconds(elapsed_seconds)}"
    )


def run_with_a_diff_file(
    diff_file: Path,
    target_language: str,
    config: config.Config,
    output_file: Path,
    extra_user_prompt: str,
) -> None:
    util_print.print_section("Reading Single 'diff' file")
    diff_file_content = _read_input_file(path_to_file=diff_file)

    _summarize_differences(
        before_file_content=diff_file_content,
        after_file_content="",
        config=config,
        target_language=target_language,
        output_file=output_file,
        extra_user_prompt=extra_user_prompt,
    )


def run_with_a_before_and_after_file(
    path_to_before_file: Path,
    path_to_after_file: Path,
    target_language: str,
    config: config.Config,
    output_file: Path,
    start_page: int,
    end_page: int,
    extra_user_prompt: str,
) -> None:
    util_print.print_section("Reading Before/After Files")

    before_file_content = _read_input_file(
        path_to_file=path_to_before_file, start_page=start_page, end_page=end_page
    )
    after_file_content = _read_input_file(
        path_to_file=path_to_after_file, start_page=start_page, end_page=end_page
    )

    _summarize_differences(
        before_file_content=before_file_content,
        after_file_content=after_file_content,
        config=config,
        target_language=target_language,
        output_file=output_file,
        extra_user_prompt=extra_user_prompt,
    )
