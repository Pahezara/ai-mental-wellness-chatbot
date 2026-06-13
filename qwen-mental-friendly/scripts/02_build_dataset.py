import json
from pathlib import Path
from transformers import AutoTokenizer

MODEL = "Qwen/Qwen2.5-7B-Instruct"

inp = Path("data/raw/train.jsonl")
outp = Path("data/processed/train.jsonl")
outp.parent.mkdir(parents=True, exist_ok=True)

tok = AutoTokenizer.from_pretrained(MODEL, use_fast=True)

def to_text(messages):
    return tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)

count = 0
with inp.open("r", encoding="utf-8") as fin, outp.open("w", encoding="utf-8") as fout:
    for line in fin:
        obj = json.loads(line)
        fout.write(json.dumps({"text": to_text(obj["messages"])}, ensure_ascii=False) + "\n")
        count += 1

print(f"Wrote {count} rows to {outp}")