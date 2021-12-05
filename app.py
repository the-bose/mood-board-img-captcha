from flask import Flask, render_template, url_for, redirect, request, send_file
from werkzeug.utils import secure_filename
from stegmod import encode, decode
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

@app.route("/stego")
def stego_view():
    return render_template("stego.html")

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

@app.route("/genstego", methods=['GET', 'POST'])
def genstego():
    inputs = request.form if request.json is None else request.json
    print(inputs)
    query = inputs["query"]
    stegotext = inputs["stegotext"]
    key = inputs["key"]
    count = int(inputs["count"])
    bgc = hex2rgb(inputs["bgc"])
    print(bgc)
    (filename, b64) = generate_coll(query, count, bgc)
    # Return file
    # return send_file(io.BytesIO(),mimetype='image/jpeg', as_attachment=True, f'static/outputs/{filename}', attachment_filename=filename)
    # Encrypt and encode message
    (enc_filename, enc_b64) = encode(f"static/outputs/{filename}", stegotext)
    # Get b64 of encoded image
    return {'name':enc_filename, 'prefix':"data:image/jpeg;base64,", 'img':enc_b64}

@app.route("/destego", methods=['GET', 'POST'])
def destego():
    inputs = request.form if request.json is None else request.json
    print(inputs)
    img = request.files["file-0"]
    fname = f"static/inputs/{secure_filename(img.filename)}"
    img.save(fname)
    dectext = decode(fname)
    success = True
    return {'decoded':dectext, 'success':success}

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
