from flask import Flask, render_template, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
import os

app = Flask(__name__)

# Set secret key for session management and CSRF protection
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Check for the OpenAI API key
if not os.getenv("API_KEY"):
    raise Exception("Please set the API_KEY environment variable.")

# Initialize the language model
llm = ChatOpenAI(temperature=0.7, api_key=os.getenv('API_KEY'))

# Initialize the conversation chain
conversation = ConversationChain(llm=llm)

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[]
)
limiter.init_app(app)

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Only 5 trials allowed per user'}), 429

@app.errorhandler(400)
def bad_request_handler(e):
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(500)
def internal_error_handler(e):
    return jsonify({'error': 'An internal error occurred'}), 500

# Apply a rate limit to the /chat route
@app.route('/chat', methods=['POST'])
@limiter.limit("5 per day")  # Limit to 5 messages per day per IP
def chat():
    # Validate and sanitize user input
    user_input = request.form.get('message', '').strip()
    chat_history = request.form.get('chat_history', '').strip()

    # Generate response
    prompt = f"Detect the language of user and reply in the same language and text language. {chat_history}\nUser: {user_input}\nAssistant:"
    try:
        response = conversation.run(input=prompt)
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing your request'}), 500

    return jsonify({'assistant': response})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({'status': 'Chat history cleared'})

if __name__ == "__main__":
    app.run()