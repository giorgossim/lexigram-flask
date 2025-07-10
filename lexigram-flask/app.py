from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
import random
from reset_utils import check_and_reset
import os
from datetime import datetime, timedelta

app = Flask(__name__)

WORDS_FILE = 'words.json'
ARCHIVE_FOLDER = "archive"
RESET_INTERVAL_HOURS = 24
MAX_WORDS = 100

# ------------ Λειτουργίες για διαχείριση λέξεων ------------

def load_words():
    try:
        with open(WORDS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_words(words):
    with open(WORDS_FILE, 'w') as f:
        json.dump(words, f)

# ------------ Λειτουργίες για reset & αρχειοθέτηση ------------

def last_reset_time():
    if os.path.exists("last_reset.txt"):
        with open("last_reset.txt", "r") as f:
            return datetime.fromisoformat(f.read().strip())
    return datetime.now()

def update_reset_time():
    with open("last_reset.txt", "w") as f:
        f.write(datetime.now().isoformat())

def archive_words():
    if not os.path.exists(ARCHIVE_FOLDER):
        os.makedirs(ARCHIVE_FOLDER)
    words = load_words()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"{ARCHIVE_FOLDER}/archive_{timestamp}.json", "w") as f:
        json.dump(words, f)
    save_words([])

def check_and_reset():
    reset_needed = False
    if datetime.now() - last_reset_time() > timedelta(hours=RESET_INTERVAL_HOURS):
        reset_needed = True
    else:
        words = load_words()
        if len(words) >= MAX_WORDS:
            reset_needed = True

    if reset_needed:
        archive_words()
        update_reset_time()

# ------------ Διαδρομές (routes) ------------

@app.route('/')
def index():
    return redirect(url_for('input_page'))

@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        word = request.form.get('word', '').strip()
        if word and len(word) <= 10:
            words = load_words()
            words.append(word)
            random.shuffle(words)
            save_words(words)
        return redirect(url_for('screen'))
    return render_template('input.html')

@app.route('/screen')
def screen():
    check_and_reset()
    words = load_words()
    random.shuffle(words)
    return render_template('screen.html', words=words)


@app.route('/api/words')
def api_words():
    check_and_reset()
    words = load_words()
    random.shuffle(words)
    return jsonify(words)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)



