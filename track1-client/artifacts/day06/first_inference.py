import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextStreamer,
)

MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
LOG_FILE = Path("logs/day06-inference.jsonl")
MAX_NEW_TOKENS = 80

PROMPTS = [
    "Explain AI inference in simple words.",
    "What is a token in a language model?",
    "Explain time to first token.",
    "Why do we measure model latency?",
    "Explain CPU inference in two sentences.",
]


class TimedStreamer(TextStreamer):
    def __init__(self, tokenizer):
        super().__init__(
            tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )
        self.first_token_time = None

    def on_finalized_text(self, text, stream_end=False):
        if text and self.first_token_time is None:
            self.first_token_time = time.perf_counter()

        print(text, end="", flush=True)


def run_request(model, tokenizer, prompt, request_number):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": request_id,
        "request_number": request_number,
        "model": MODEL_ID,
        "prompt": prompt,
        "prompt_tokens": None,
        "output_tokens": None,
        "ttft_seconds": None,
        "total_time_seconds": None,
        "failure": None,
    }

    print(f"\n--- Request {request_number}/5 ---")
    print(f"Request ID: {request_id}")

    try:
        messages = [{"role": "user", "content": prompt}]

        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
        )

        prompt_tokens = inputs["input_ids"].shape[1]
        record["prompt_tokens"] = prompt_tokens

        streamer = TimedStreamer(tokenizer)

        print(f"Prompt tokens: {prompt_tokens}")
        print("Response: ")

        with torch.inference_mode():
            output = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
                streamer=streamer,
            )

        end_time = time.perf_counter()

        generated_ids = output[0, inputs["input_ids"].shape[1]:]
        output_tokens = generated_ids.shape[0]

        record["output_tokens"] = output_tokens
        record["total_time_seconds"] = round(end_time - start_time, 4)

        if streamer.first_token_time is not None:
            record["ttft_seconds"] = round(
                streamer.first_token_time - start_time, 4
            )

        print(f"\nOutput tokens: {output_tokens}")
        print(f"Total time: {record['total_time_seconds']} seconds")
        print(f"TTFT: {record['ttft_seconds']} seconds")

    except Exception as exc:
        record["failure"] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
        record["total_time_seconds"] = round(
            time.perf_counter() - start_time, 4
        )
        print(f"Request failed: {type(exc).__name__}: {exc}")

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


def main():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    print("Loading model on CPU...")
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
    model.to("cpu")
    model.eval()

    results = []

    for number, prompt in enumerate(PROMPTS, start=1):
        results.append(
            run_request(model, tokenizer, prompt, number)
        )

    successful = sum(
        1 for result in results if result["failure"] is None
    )
    failed = len(results) - successful

    print("\n--- Summary ---")
    print(f"Total requests: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Failure rate: {failed / len(results) * 100:.1f}%")
    print(f"Log saved to: {LOG_FILE}")


if __name__ == "__main__":
    main()
