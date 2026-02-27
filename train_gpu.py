import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    DataCollatorForSeq2Seq
)
from datasets import Dataset
import json
from sklearn.model_selection import train_test_split

# CHECK GPU
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("Number of GPUs:", torch.cuda.device_count())
    print("Current GPU memory (GB):", torch.cuda.memory_allocated(0) / 1024**3)
else:
    print("GPU not detected! Falling back to CPU.")

# LOAD DATA
def load_data(file_path="data/training_data_phot5.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} samples")
    return data

# Chia train/val (90/10)
data = load_data()
train_data, val_data = train_test_split(data, test_size=0.1, random_state=42)
train_dataset = Dataset.from_list(train_data)
val_dataset = Dataset.from_list(val_data)
print(f"Train samples: {len(train_dataset)}, Val samples: {len(val_dataset)}")

# PREPROCESS
def preprocess_function(examples, tokenizer):
    inputs = examples["input_text"]
    targets = examples["target_text"]

    model_inputs = tokenizer(
        inputs,
        max_length=192,
        truncation=True,
        padding="max_length"
    )

    labels = tokenizer(
        text_target=targets,
        max_length=128,
        truncation=True,
        padding="max_length"
    )

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# MAIN
if __name__ == "__main__":
    model_name = "VietAI/vit5-base"

    print("Loading tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")

    # Tokenize train và val
    tokenized_train = train_dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=train_dataset.column_names
    )
    tokenized_val = val_dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=val_dataset.column_names
    )

    # Data collator cho seq2seq
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding=True
    )

    training_args = Seq2SeqTrainingArguments(
        output_dir="models/vit5_finetuned_gpu",
        evaluation_strategy="epoch",
        learning_rate=1e-4,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        gradient_accumulation_steps=2,
        num_train_epochs=8,
        weight_decay=0.01,
        warmup_steps=500,
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        fp16=True,
        logging_steps=20,
        report_to="none",
        optim="adamw_torch",
        dataloader_num_workers=2,
        predict_with_generate=True,
        push_to_hub=False,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    print("Starting GPU fine-tune...")
    trainer.train()

    trainer.save_model("models/vit5_finetuned_gpu")
    tokenizer.save_pretrained("models/vit5_finetuned_gpu")

    print("Training completed on GPU!")