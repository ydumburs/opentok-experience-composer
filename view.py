import os
import webbrowser
from dotenv import load_dotenv
from flask import Flask, render_template_string
from threading import Timer

load_dotenv()
app = Flask(__name__)


@app.route("/publish")
def publish():
    with open("publish.html") as f:
        html = f.read()
        html_filled = html.replace("{{API_KEY}}", os.getenv("VIDEO_PROJECT_API_KEY")) \
            .replace("{{SESSION_ID}}", os.getenv("VIDEO_SESSION_ID")) \
            .replace("{{TOKEN}}", os.getenv("VIDEO_TOKEN"))
    return render_template_string(html_filled)


@app.route("/subscribe")
def subscribe():
    with open("subscribe.html") as f:
        html = f.read()
        html_filled = html.replace("{{API_KEY}}", os.getenv("VIDEO_PROJECT_API_KEY")) \
            .replace("{{SESSION_ID}}", os.getenv("VIDEO_SESSION_ID")) \
            .replace("{{TOKEN}}", os.getenv("VIDEO_TOKEN"))
    return render_template_string(html_filled)


def open_browser():
    webbrowser.open_new("http://localhost:8080/subscribe")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(port=8080)
