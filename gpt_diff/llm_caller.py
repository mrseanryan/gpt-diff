import json
import requests

from cornsnake import util_print

from gpt_diff import config, prompts

def _filter_out_thinking(result_str: str, config:config.Config) -> str:
    if len(config.model_thinking_tag):
        xml_end_tag = f"</{config.model_thinking_tag}>"
        start = result_str.find(xml_end_tag)
        if start == -1:
            return result_str  # No end tag found
        
        end = start + len(xml_end_tag)
        return result_str[end+1:].lstrip()

    return result_str

def call_llm(before_file:str, after_file:str, config: config.Config) -> str:

    # Request payload with streaming enabled
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": prompts.system_prompt},
            {"role": "user", "content": prompts.build_user_message(before_file, after_file)}
        ],
        "stream": True
    }

    # Send streaming request
    result_str = ""
    has_finished_thinking = False
    does_thinking = len(config.model_thinking_tag) > 0
    with requests.post(config.ollama_url, json=payload, stream=True) as response:
        if response.status_code == 200:
            print("AI > ", end=" ", flush=True)
            for line in response.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    # Each line is a separate JSON object
                    chunk = json.loads(data)
                    content = chunk.get("message", {}).get("content", "")

                    result_str += content + "\n"

                    has_finished_thinking = not(does_thinking) or (f"</{config.model_thinking_tag}>" in result_str)

                    if has_finished_thinking or config.is_verbose:
                        content_to_print = _filter_out_thinking(result_str=content, config=config)
                        print(content_to_print, end="", flush=True)
                    else:
                        print(".", end="", flush=True)
            if config.is_verbose:
                print()  # Final newline
            result_str += "\n"
        else:
            print("Error:", response.status_code, response.text)

    return _filter_out_thinking(result_str=result_str, config=config)
