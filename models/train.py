from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, AutoModelForCausalLM, AutoTokenizer

mbart_tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
mbart_model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

jamba_model = AutoModelForCausalLM.from_pretrained("ai21labs/Jamba-v0.1")
jamba_tokenizer = AutoTokenizer.from_pretrained("ai21labs/Jamba-v0.1")

def translate(text, src_lang, tgt_lang):
    """Translate text from source language to target language using MBart."""
    mbart_tokenizer.src_lang = src_lang
    encoded_text = mbart_tokenizer(text, return_tensors="pt", padding=True)
    generated_tokens = mbart_model.generate(**encoded_text, forced_bos_token_id=mbart_tokenizer.lang_code_to_id[tgt_lang])
    return mbart_tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

def generate_text(prompt, max_length=50):
    """Generate text using Jamba model."""
    input_ids = jamba_tokenizer("In the recent Super Bowl LVIII,", return_tensors='pt').to(jamba_model.device)["input_ids"]
    outputs = jamba_model.generate(input_ids, max_new_tokens=216)

def process_text(user_input, user_lang):
    """Process text: translate, generate, and translate back."""
    # Identify the language (assuming user_lang is in ISO format)
    # Step 2: Translate to English
    english_text = translate(user_input, user_lang, "en_XX")
    
    # Step 3: Generate text with Jamba
    generated_text = generate_text(english_text)
    
    # Step 4: Translate the generated text back to the original language
    final_text = translate(generated_text, "en_XX", user_lang)

    return final_text

# Example usage
user_input = "Hallo, wie geht es dir?"
user_lang = "de_DE"
result = process_text(user_input, user_lang)
print(result)
