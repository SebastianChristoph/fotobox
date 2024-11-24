from flask import Flask, render_template, request
import os

app = Flask(__name__)

text_to_show = ""
font_style = ""

@app.route("/", methods=["GET"] )
def home():
    return render_template("home.html")

@app.route("/preview", methods=["GET"] )
def preview():
    return render_template("preview.html")

@app.route("/personalize", methods=["GET", "POST"] )
def personalize():
    global text_to_show, font_style
    if request.method == "POST":
        text_to_show = request.form.get("text_to_show")
        font_style = request.form.get("font_style")
        print(f"Set global text to show to: {text_to_show}")
        print(f"Set global font_style to: {font_style}")
    

    return render_template("personalize.html", text_to_show = text_to_show, font_style = font_style)

@app.route("/chooseframe", methods=["GET"] )
def choose_frame():
    return render_template("choose_frame.html")

@app.route("/addtext", methods=["GET"] )
def add_text():
    return render_template("add_text.html", text_to_show = text_to_show)

if __name__ == "__main__":
    app.run(debug=True)

