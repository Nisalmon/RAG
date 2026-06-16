from transformers import (AutoModelForCausalLM,
                          AutoTokenizer, PreTrainedModel)
import os


class Model:
    model: PreTrainedModel

    def __init__(self) -> None:
        cache_dir = f"/goinfre/{os.getenv('USER')}/.cache/huggingface"
        self.model_name: str = "Qwen/Qwen3-0.6B"
        self.model: PreTrainedModel = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            cache_dir=cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name,
                                                       cache_dir=cache_dir)
