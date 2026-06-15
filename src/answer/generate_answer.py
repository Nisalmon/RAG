from llm_sdk import Model
from typing import Any, List, Generator
import torch


def generate_answer(model: Model, prompt: str):

    full_prompt = (
        "<|im_start|>user\n"
        + prompt
        + "\nOnly give the answer.\n"
        + "<|im_end|>\n"
        + "<|im_start|>assistant\n<think>\n\n</think>\n\n"
    )

    inputs = model.tokenizer(full_prompt, return_tensors="pt")

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        output = model.model.generate(input_ids,
                                      attention_mask=attention_mask,
                                      max_new_tokens=256,
                                      num_return_sequences=1,
                                      use_cache=True,
                                      eos_token_id=model.tokenizer.eos_token_id,
                                      pad_token_id=model.tokenizer.eos_token_id
                                    )

    input_len = input_ids.shape[1]
    generated_text = output[0][input_len:]

    return (model.tokenizer.decode(generated_text, skip_special_tokens=True))
