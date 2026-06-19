import requests
import json 
import csv
import ast
import re

def generate_fc(notes_text, num_card =5):

    prompt = f'''Read the folllowing notes and generate exactly {num_card} flashcards
Return ONLY the python list od dictionaries in this exact format, nothing else:
[
    {{"question":"...","answer":"..."}}
    {{"question":"...","answer":"..."}}
]

Notes:
{notes_text}'''
    response = requests.post(
        "http://localhost:11434/api/chat",
        json ={
            'model':'mistral',
            'messages':[{'role':'user','content':prompt}],
            'stream':False 
        }
    )
    return response.json()['message']['content']


def parse_fc(ai_text):
    cleaned = ai_text.strip()
    start = cleaned.find('[')
    end = cleaned.rfind(']') + 1
    cleaned = cleaned[start:end]
    cleaned = re.sub(r'}\s*\n\s*{', '},\n{', cleaned)
    
    try:
        return json.loads(cleaned)
    except:
        return ast.literal_eval(cleaned)


def save_csv(deck, filename='flashcards.csv'):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=["question", "answer"])
        writer.writeheader()
        writer.writerows(deck)
        print(f'Saved {len(deck)} cards to {filename}')



def display_card(deck):
    for i,card in enumerate(deck, start=1):
        print(f"card {i}")
        print(f" Q:{card['question']}")
        print(f" A:{card['answer']}")
        print()

def add_card(deck,question,answer):
    new_card = {
        'Question':question,
        'Answer': answer
    }
    deck.append(new_card)
    return deck

def read_notes(filename):
    with open (filename, "r") as f:
        content = f.read()
    return content

def preview_text(text, max_char = 300):
    if len(text)> max_char:
        print(text[:max_char]+'...')
    else:
        print(text)

#------MAIN PROGRAM-------

notes = read_notes('notes.txt')
print(f'Loaded {len(notes)} charactersof notes.')
print()

print('Asking Mistral to generate Flashcards')
result = generate_fc(notes, num_card =5)

print('=== AI RESPONSE ===  ')
print(result)
print()

print("Parsing flashcards...")
deck = parse_fc(result)

print("=== Your Flashcards ===")
display_card(deck)

save_csv(deck)





'''notes = read_notes('notes.txt')

print("=== Notes loaded! ===")
print(f"Total characters: {len(notes)}")
print()
print("=== Preview ===")
preview_text(notes)'''



'''my_deck = []
my_deck = add_card(my_deck, "What is a variable?", "A named container that stores a value")
my_deck = add_card(my_deck, "What does a for loop do?", "Repeats code for each item in a sequence")
my_deck = add_card(my_deck, "What is a dictionary?", "A collection of key-value pairs")

display_card(my_deck)
print(f'Total Cards {len(my_deck)}')'''