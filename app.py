from flask import Flask, render_template, url_for, redirect, send_file
from generator import generate

app = Flask(__name__)
app.config['SECRET KEY'] = '3E8FBFF793F7FAF1E194288542CBA'

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/generate")
def generate():
    inputs = request.json
    query = inputs["query"]
    key = inputs["key"]
    count = int(inputs["count"])
    bgc = inputs["bgc"]
    filename = generate(query, count, bgc)
    return send_file(f'static/outputs/{filename}', attachment_filename=filename)

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
