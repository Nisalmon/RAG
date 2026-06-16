from llm_sdk import Model
import torch
from torch.nn.modules import Module


def generate_answer(model: Model, prompt: str) -> str:

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
        eos = model.tokenizer.eos_token_id
        pad = model.tokenizer.eos_token_id
        if not isinstance(model.model.generate, Module):
            return ""
        output = model.model.generate(input_ids,
                                      attention_mask=attention_mask,
                                      max_new_tokens=256,
                                      num_return_sequences=1,
                                      use_cache=True,
                                      eos_token_id=eos,
                                      pad_token_id=pad
                                      )

    input_len = input_ids.shape[1]
    generated_text = output[0][input_len:]

    return str(model.tokenizer.decode(
        generated_text, skip_special_tokens=True))
