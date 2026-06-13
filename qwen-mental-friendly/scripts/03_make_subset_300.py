from pathlib import Path

SRC = Path("data/processed/train.jsonl")
DST = Path("data/processed/train_300.jsonl")

n = 300
with SRC.open("r", encoding="utf-8") as fin, DST.open("w", encoding="utf-8") as fout:
    for i, line in enumerate(fin):
        if i >= n:
            break
        fout.write(line)

print(f"Wrote {min(n, i+1)} lines to {DST}")