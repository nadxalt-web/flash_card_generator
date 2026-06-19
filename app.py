from flask import Flask, request, jsonify, render_template
import requests
import json
import re
import csv

app = Flask(__name__)

def generate_fc(notes_text, num_cards=5):
    prompt = f"""Read the following notes and generate exactly {num_cards} flashcards.
Return ONLY a Python list of dictionaries in this exact format, nothing else:
[
  {{"question":"...","answer":"..."}},
  {{"question":"...","answer":"..."}}
]
Notes:
{notes_text}"""

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "mistral",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    )
    raw = response.json()["message"]["content"]
    start = raw.find('[')
    end = raw.rfind(']') + 1
    cleaned = raw[start:end]
    cleaned = re.sub(r'}\s*\n\s*{', '},\n{', cleaned)
    return json.loads(cleaned)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    notes = data['notes']
    num_cards = int(data.get('num_cards', 5))
    cards = generate_fc(notes, num_cards)
    return jsonify(cards)

if __name__ == '__main__':
    app.run(debug=True)