from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize Flask app
app = Flask(__name__)

# Load a pre-trained language model and tokenizer for text generation
model_name = "gpt2"  # You can replace this with another suitable model if needed
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define the route for the text generation API
@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        # Get the input prompt from the JSON payload
        data = request.json
        input_prompt = data.get('input_prompt', '')

        if not input_prompt:
            return jsonify({'error': 'No input prompt provided'}), 400

        # Tokenize the input text
        inputs = tokenizer(input_prompt, return_tensors="pt")

        # Generate text based on the input prompt
        generated_outputs = model.generate(
            inputs.input_ids,
            max_length=4096,  # Adjust the max_length as needed
            num_return_sequences=1,  # Number of sequences to generate
            no_repeat_ngram_size=2,  # Prevent repeating n-grams
            early_stopping=True
        )

        # Decode the generated tokens to text
        generated_text = tokenizer.decode(generated_outputs[0], skip_special_tokens=True)

        # Return the generated text as a JSON response
        return jsonify({'generated_text': generated_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
