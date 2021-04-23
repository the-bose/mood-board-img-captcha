from flask import Flask, render_template, url_for, redirect, request, send_file
from colormap import hex2rgb
from generator import generate_coll

app = Flask(__name__)
app.config['SECRET KEY'] = '3E8FBFF793F7FAF1E194288542CBA'

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/captcha")
def captcha():
    return render_template("captcha.html")

@app.route("/generate", methods=['GET', 'POST'])
def generate():
    inputs = request.form
    print(inputs)
    query = inputs["query"]
    key = inputs["key"]
    count = int(inputs["count"])
    bgc = hex2rgb(inputs["bgc"])
    print(bgc)
    filename = generate_coll(query, count, bgc)
    return send_file(f'static/outputs/{filename}', attachment_filename=filename)

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
