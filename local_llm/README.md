# Local LLM README (via Ollama)

This README describes how to run a local LLM for use by gpt-diff, to ensure data privacy.

## Setup

1. [Install Ollama](https://ollama.com/download)

2. Install a suitable LLM model

There are many LLM families and models.

As of June 2025 [Qwen family](https://huggingface.co/Qwen) have many small models.

- https://huggingface.co/Qwen/Qwen3-8B [5 Gb download] seems a good option for comparing text files.

```bash
ollama list
ollama pull qwen3:8b
ollama list
```

3. Configure gpt-diff

Edit [config.py](../gpt_diff/config.py) to suit - in particular, you need to set the model id to match the model you are using with ollama.
