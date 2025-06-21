def build_system_prompt(target_language: str) -> str:
    prompt = "You are gpt-diff an expert at examining 2 files and summarising their differences. If there is just 1 file then try to process it as a diff file (for example from git diff)."

    if target_language:
        prompt += f"\nAlways respond in the {target_language} language."

    return prompt


def build_user_message(before_file: str, after_file: str) -> str:
    return f"Describe the before and after differences between these 2 files.\n\nBEFORE:\n{before_file}\n\nAFTER:\n{after_file}\n"
