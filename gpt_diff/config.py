from dataclasses import dataclass, field


@dataclass
class Config:
    # Model name (make sure it's pulled via `ollama pull <model>`)
    model: str = field(default="qwen3:8b")
    model_thinking_tag: str = field(
        default="think"
    )  # Does the model output '<think>' tag - anything there will be filtered out. Set to empty to disable the filtering.

    # Ollama API endpoint
    ollama_url: str = field(default="http://localhost:11434/api/chat")

    is_verbose: bool = field(default=False)


def read_config() -> Config:
    # TODO add a config reader, read from config.ini
    return Config()
