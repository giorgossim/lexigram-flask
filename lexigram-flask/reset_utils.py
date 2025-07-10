import os
import json
from datetime import datetime, timedelta

ARCHIVE_FOLDER = "archive"
MAX_WORDS = 100  # ή ό,τι όριο θέλεις
RESET_INTERVAL_HOURS = 24

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

    if os.path.exists("words.json"):
        with open("words.json", "r") as f:
            words = json.load(f)
        if words:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"{ARCHIVE_FOLDER}/archive_{timestamp}.json", "w") as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
            with open("words.json", "w") as f:
                json.dump([], f)

def check_and_reset():
    reset_needed = False

    if datetime.now() - last_reset_time() > timedelta(hours=RESET_INTERVAL_HOURS):
        reset_needed = True
    else:
        if os.path.exists("words.json"):
            with open("words.json", "r") as f:
                words = json.load(f)
                if len(words) >= MAX_WORDS:
                    reset_needed = True

    if reset_needed:
        archive_words()
        update_reset_time()
