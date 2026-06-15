from transformers import (AutoModelForCausalLM,
                          AutoTokenizer)
import os


class Model:
    def __init__(self):
        cache_dir = f"/goinfre/{os.getenv('USER')}/.cache/huggingface"
        self.model_name: str = "Qwen/Qwen3-0.6B"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name,
                                                          cache_dir=cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name,
                                                       cache_dir=cache_dir)
