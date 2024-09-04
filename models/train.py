# Import necessary libraries
import torch
from transformers import (
    MBartForConditionalGeneration,
    MBart50TokenizerFast,
    AutoModelForCausalLM,
    AutoTokenizer
)
from langdetect import detect
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if CUDA is available and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Load MBart50 model and tokenizer for translation
try:
    mbart_tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    mbart_model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt").to(device)
    logger.info("Successfully loaded MBart50 model and tokenizer.")
except Exception as e:
    logger.error(f"Error loading MBart50 model: {e}")
    raise

# Define available models for text generation
models = [
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
    "mistralai/Mistral-7B-v0.1",
    "microsoft/phi-1_5",
    "microsoft/Orca-2-7b",
]

# Choose a model (ensure the index is within range)
choice = -2  # Changed to use a smaller model for demonstration
selected_model_name = models[choice]

# Load the selected language model and tokenizer
try:
    model_tokenizer = AutoTokenizer.from_pretrained(selected_model_name)
    model_model = AutoModelForCausalLM.from_pretrained(selected_model_name).to(device)
    logger.info(f"Successfully loaded model: {selected_model_name}")
except Exception as e:
    logger.error(f"Error loading model {selected_model_name}: {e}")
    raise

def translate(text, src_lang, tgt_lang):
    try:
        mbart_tokenizer.src_lang = src_lang
        encoded_text = mbart_tokenizer(text, return_tensors="pt").to(device)
        generated_tokens = mbart_model.generate(
            **encoded_text,
            forced_bos_token_id=mbart_tokenizer.lang_code_to_id[tgt_lang],
            max_length=512,
            num_beams=5,
            early_stopping=True
        )
        translated_text = mbart_tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        logger.info(f"Translated '{text}' from {src_lang} to {tgt_lang}: '{translated_text}'")
        return translated_text
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        return None

def generate_text(prompt, max_length=200):
    try:
        input_ids = model_tokenizer.encode(prompt, return_tensors='pt').to(device)
        outputs = model_model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
        generated_text = model_tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Generated text for prompt '{prompt}': '{generated_text}'")
        return generated_text
    except Exception as e:
        logger.error(f"Error during text generation: {e}")
        return None

def process_text(user_input, user_lang):
    # Detect language if not provided
    if not user_lang:
        user_lang = detect(user_input)
        logger.info(f"Detected language: {user_lang}")
    
    # Map user_lang to MBart50 language codes
    lang_code_map = {
        "hi": "hi_IN",
        "en": "en_XX",
        # Add more language codes as needed
    }
    
    src_lang_code = lang_code_map.get(user_lang[:2], "en_XX")
    
    # Translate user input to English
    english_text = translate(user_input, src_lang_code, "en_XX")
    if not english_text:
        return "Error in translation step."
    
    # Generate text based on English prompt
    generated_text = generate_text(english_text)
    if not generated_text:
        return "Error in text generation step."
    
    # Translate generated text back to user's language
    final_text = translate(generated_text, "en_XX", src_lang_code)
    if not final_text:
        return "Error in final translation step."
    
    return final_text

if __name__ == "__main__":
    user_input = "नमस्ते, आप कैसे हैं?"
    user_lang = "hi"
    result = process_text(user_input, user_lang)
    print(f"Final output: {result}")
