from flask import Flask, render_template, request, Response
import os
from camera_pi import Camera
import subprocess
from datetime import datetime
import cups
import img_edit

app = Flask(__name__)

text_to_show = ""
font_style = ""
current_img = ""
current_img_path = ""

def print_image():
    image_path = f"/home/pi/fotobox/static/images/{current_img}"
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = list(printers.keys())[0]
    conn.printFile(printer_name, image_path , "Photo Booth", {})

@app.route("/", methods=["GET"] )
def home():   
    return render_template("home.html")

@app.route("/preview", methods=["GET"] )
def preview():
    return render_template("preview.html")

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take-picture')
def take_picture():
    global current_img
    current_img = ""
    now = datetime.now()
    img_name = now.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
    current_img = img_name
    current_img_path = f'static/images/{img_name}'
    img_edit.resize_img(current_img_path)
    img_edit.add_text_to_image(current_img_path, text_to_show, "Normal")

    subprocess.run(['gphoto2', '--capture-image-and-download',  '--filename', f'static/images/{img_name}'])
    return render_template('show_img.html', img_name = img_name)

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

@app.route("/print", methods=["GET"] )
def print():
    global current_img
    print_image()
    return render_template("print.html", img_name = current_img)

if __name__ == "__main__":
    app.run(debug=True)

