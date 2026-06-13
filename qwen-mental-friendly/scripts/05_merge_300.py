from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE = "Qwen/Qwen2.5-7B-Instruct"
ADAPTER = "outputs/qwen-friendly-lora-300"
OUT = "merged/qwen-friendly-merged-300"

Path(OUT).mkdir(parents=True, exist_ok=True)

tok = AutoTokenizer.from_pretrained(BASE, use_fast=True)

base = AutoModelForCausalLM.from_pretrained(
    BASE,
    torch_dtype=torch.float16,
    device_map="cpu",
    low_cpu_mem_usage=True,
)

m = PeftModel.from_pretrained(base, ADAPTER)
m = m.merge_and_unload()

m.save_pretrained(
    OUT,
    safe_serialization=True,
    max_shard_size="1GB",
)
tok.save_pretrained(OUT)

print("Merged model saved to:", OUT)