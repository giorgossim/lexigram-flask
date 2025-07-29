from flask import Flask, render_template, request, redirect, jsonify
import json
import os
import random

app = Flask(__name__)

WORDS_FILE = "words.json"

# 1. Load words from file (or start empty)
if os.path.exists(WORDS_FILE):
    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        words = json.load(f)
else:
    words = []

@app.route("/", methods=["GET", "POST"])
def index():
    global words
    if request.method == "POST":
        new_word = request.form.get("word", "").strip()
        if new_word:
            words.append(new_word)
            save_words()
        return render_template("thankyou.html")  # We'll create this file
    return render_template("input.html")

@app.route("/display")
def display():
    shuffled_words = words[:]
    random.shuffle(shuffled_words)
    return render_template("screen.html", words=shuffled_words)

@app.route("/reset")
def reset():
    key = request.args.get("key")
    if key == "your_secret_key":  # CHANGE THIS to something private
        global words
        words = []
        save_words()
        return "Words reset."
    return "Unauthorized.", 401

@app.route("/api/words")
def api_words():
    return jsonify(words)

def save_words():
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    app.run(debug=True)




