import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
from datasets import load_dataset

dataset = load_dataset("facebook/flores", "all", trust_remote_code=True)


model_name = "EleutherAI/gpt-neo-125M"  # You can choose other sizes like 1.3B or 2.7B
model = GPTNeoForCausalLM.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Step 5: Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir="./results",          # Where to store the final model.
    evaluation_strategy="epoch",     # Evaluation is done at the end of each epoch.
    learning_rate=2e-5,
    weight_decay=0.01,
    num_train_epochs=3,
    per_device_train_batch_size=2,   # Adjust based on your GPU memory.
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    tokenizer=tokenizer
)

# Step 7: Fine-tune the model
trainer.train()

# Step 8: Save the fine-tuned model
model.save_pretrained("./fine-tuned-model")
tokenizer.save_pretrained("./fine-tuned-model")