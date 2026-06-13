import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    Trainer,
)
from peft import LoraConfig, get_peft_model


BASE = "Qwen/Qwen2.5-7B-Instruct"
DATA = "data/processed/train_300.jsonl"
OUT  = "outputs/qwen-friendly-lora-300"

MAX_LEN = 1024


def main():
    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )

    tokenizer = AutoTokenizer.from_pretrained(BASE, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(
        BASE,
        device_map="auto",
        quantization_config=bnb,
        torch_dtype=torch.float16,
    )
    model.config.use_cache = False
    model.gradient_checkpointing_enable()

    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    )
    model = get_peft_model(model, lora)

    ds = load_dataset("json", data_files=DATA, split="train")

    def tokenize_fn(batch):
        out = tokenizer(
            batch["text"],
            truncation=True,
            max_length=MAX_LEN,
            padding="max_length",
        )
        return out

    ds_tok = ds.map(tokenize_fn, batched=True, remove_columns=ds.column_names)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    args = TrainingArguments(
        output_dir=OUT,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=8e-5,
        num_train_epochs=1,
        logging_steps=5,
        save_steps=100,
        save_total_limit=2,
        fp16=True,
        report_to="none",
        optim="paged_adamw_8bit",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds_tok,
        data_collator=data_collator,
    )

    trainer.train()
    model.save_pretrained(OUT)
    tokenizer.save_pretrained(OUT)
    print("Saved LoRA adapter:", OUT)


if __name__ == "__main__":
    main()