from flask import Flask, request, jsonify
from difflib import get_close_matches

app = Flask(__name__)

def get_best_match(user_question: str, questions: dict) -> str | None:
    """Compares the user message similarity to the ones in the dictionary"""

    questions: list[str] = [q for q in questions]
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)

    # Return the first best match, else return None
    if matches:
        return matches[0]

@app.route('/')
def index():
    return 'Welcome to my Flask Chatbot!'

@app.route('/chatbot', methods=['POST'])
def chatbot():
    knowledge = {
        'hello': 'Hey there!',
        'how are you?': 'I am good, thanks!',
        'do you know what the time is?': 'Not at all!',
        'what time is it?': 'No clue!',
        'what can you do?': 'I can answer questions!',
        'ok': 'Great.'
    }

    user_input = request.json.get('message', '')

    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        return jsonify({'response': 'Goodbye!'})

    # Finds the best match, otherwise returns None
    best_match = get_best_match(user_input, knowledge)

    # Gets the best match from the knowledge base
    if best_match:
        answer = knowledge.get(best_match)
        return jsonify({'response': answer})
    else:
        return jsonify({'response': 'I don\'t understand... Could you try rephrasing that?'})

if __name__ == "__main__":
    app.run(debug=True)
