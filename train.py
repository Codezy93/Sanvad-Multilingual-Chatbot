from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset, Dataset, DatasetDict
import pandas as pd
import torch

# Define the languages
languages = ["hi", "te", "ta", "ml", "kn", "bn", "mr", "gu", "or"]

# Load the tokenizer and model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to load vocab
def load_vocab(language_code):
    vocab_path = f"./dataset/vocab/{language_code}.tsv"
    vocab_df = pd.read_csv(vocab_path, sep="\t")
    return vocab_df

# Function to load corpus
def load_corpus(language_code):
    corpus_path = f"./dataset/corpus/{language_code}.txt"
    with open(corpus_path, 'r', encoding='utf-8') as file:
        corpus = file.readlines()
    return corpus

# Function to create dataset for training
def create_dataset(language_code):
    vocab = load_vocab(language_code)
    corpus = load_corpus(language_code)
    data = {"text": corpus}
    return Dataset.from_dict(data)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

# Function to train and save model
def train_and_save_model(language):
    # Load and prepare dataset
    dataset = create_dataset(language)
    tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    
    # Define training arguments
    training_args = TrainingArguments(
        output_dir=f"./results/{language}",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir=f"./logs/{language}",
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
    )
    
    # Train model
    trainer.train()
    
    # Save model
    trainer.save_model(f"./models/{language}")

# Train and save model for each language
for language in languages:
    print(f"Training model for {language}...")
    train_and_save_model(language)
    print(f"Model for {language} saved.")

print("All models trained and saved successfully.")