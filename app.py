from flask import Flask, render_template, url_for, redirect, request, send_file
from colormap import hex2rgb
from generator import generate_coll
import base64

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
    inputs = request.form if request.json is None else request.json
    print(inputs)
    query = inputs["query"]
    key = inputs["key"]
    count = int(inputs["count"])
    bgc = hex2rgb(inputs["bgc"])
    print(bgc)
    (filename, b64) = generate_coll(query, count, bgc)
    # Return file
    # return send_file(io.BytesIO(),mimetype='image/jpeg', as_attachment=True, f'static/outputs/{filename}', attachment_filename=filename)
    return {'name': filename, 'prefix':"data:image/jpeg;base64,", 'img':b64}

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
