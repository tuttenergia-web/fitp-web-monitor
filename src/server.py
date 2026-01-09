from flask import Flask
import threading
import scraper  # importa il tuo scraper

app = Flask(__name__)

@app.route("/")
def home():
    return "Scraper running"

def run_scraper():
    scraper.poll(30)  # avvia il tuo scraper esattamente come nel main

# Avvia lo scraper in un thread separato
threading.Thread(target=run_scraper, daemon=True).start()

# Avvia un piccolo server web per Render
app.run(host="0.0.0.0", port=10000)