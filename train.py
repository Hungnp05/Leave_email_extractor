from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import Dataset
import json

def load_data(file_path="data/training_data_phot5.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} samples")
    return Dataset.from_list(data)

def preprocess_function(examples, tokenizer):
    inputs = examples["input_text"]
    targets = examples["target_text"]
    
    model_inputs = tokenizer(
        inputs,
        max_length=256,
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

if __name__ == "__main__":
    model_name = "VietAI/vit5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    dataset = load_data()
    tokenized_dataset = dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=dataset.column_names
    )
    
    training_args = Seq2SeqTrainingArguments(
        output_dir="models/vit5_finetuned",
        eval_strategy="no",
        learning_rate=1e-4,
        per_device_train_batch_size=4,
        num_train_epochs=10,
        weight_decay=0.01,
        save_strategy="epoch",
        predict_with_generate=True,
        fp16=False,
        logging_steps=10,
        report_to="none",
    )
    
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
    )
    
    print("Starting fine-tune VietAI/vit5-base...")
    trainer.train()
    trainer.save_model("models/vit5_finetuned")
    tokenizer.save_pretrained("models/vit5_finetuned")
    print("Done!")