import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

BASE = "Qwen/Qwen2.5-7B-Instruct"
ADAPTER = "outputs/qwen-friendly-lora-300"

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,
)

tok = AutoTokenizer.from_pretrained(BASE, use_fast=True)

base = AutoModelForCausalLM.from_pretrained(
    BASE,
    device_map="auto",
    quantization_config=bnb,
    torch_dtype=torch.float16,
)
model = PeftModel.from_pretrained(base, ADAPTER)
model.eval()

def chat(user: str):
    messages = [
        {"role":"system","content":"You are a supportive companion. Be warm, realistic, and human. Ask gentle questions before giving advice. Avoid clichés."},
        {"role":"user","content": user},
    ]
    prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok([prompt], return_tensors="pt").to(model.device)

    out = model.generate(
        **inputs,
        max_new_tokens=220,
        do_sample=True,
        temperature=0.95,
        top_p=0.92,
        repetition_penalty=1.08,
    )
    print(tok.decode(out[0], skip_special_tokens=True))
    print("\n" + "-"*80 + "\n")

chat("Hey. Can you talk with me for a bit?")
chat("I feel lonely at night and I overthink.")
chat("I can't sleep. My mind keeps racing.")