from flask import Flask, render_template, request, redirect
import subprocess
from datetime import datetime
import cups
import img_edit
import camera_handler

app = Flask(__name__)

text_to_show = "Tina & Sehb 2024"
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
    camera_handler.start_cam()
    return render_template("preview.html")

@app.route('/take-picture')
def take_picture():
    global current_img, current_img_path, font_style
    camera_handler.stop_cam()
    current_img = ""
    now = datetime.now()
    img_name = now.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
    current_img = img_name
    current_img_path = f'static/images/{img_name}'
    subprocess.run(['gphoto2', '--capture-image-and-download',  '--filename', f'{current_img_path}'])
    print("add text with font-style:", font_style)
    if text_to_show != "":
        img_edit.add_text_to_image(current_img_path, text_to_show, font_style)

    return render_template('show_img.html', img_name = img_name)

@app.route("/personalize", methods=["GET", "POST"] )
def personalize():
    global text_to_show, font_style
    if request.method == "POST":
        text_to_show = request.form.get("text_to_show")
        font_style = request.form.get("font_style")
      
    return render_template("personalize.html", text_to_show = text_to_show, font_style = font_style)

@app.route("/choosefont", methods=["GET"] )
def choose_font():
    return render_template("choose_font.html", text_to_show = text_to_show, font_style = font_style)

@app.route("/addtext", methods=["GET"] )
def add_text():
    return render_template("add_text.html", text_to_show = text_to_show, font_style = font_style)

@app.route("/pre-print", methods=["GET"] )
def pre_print_image_route():
    global current_img
    print_image()
    return render_template("pre-print.html", img_name = current_img)

def has_printer_errors():
    conn = cups.Connection()
    printDict =  conn.getPrinters()
    printers = conn.getPrinters()
    printer = list(printers.keys())[0]
    print("######## CHECK ERRORS ##################")
    print("printers: ", printers, "\n")
    print("dict:", printDict[printer]['printer-state-reasons'])

    error = "Kein Fehler"

    if "media-empty-error" in printDict[printer]['printer-state-reasons'] or "media-needed" in printDict[printer]['printer-state-reasons']:
        error = "Papier nachlegen, Drucker startet automatisch"
          
    elif "marker-supply-empty-error" in printDict[printer]['printer-state-reasons']:
        error = "Die Drucker-Patrone ist nicht richtig eingesetzt.Bitte überprüfen!"
           
    elif "input-tray-missing" in printDict[printer]['printer-state-reasons']:
        error="Die Papierkessette ist nicht richtig eingesetzt! Bitte überprüfen!"
    
    return error != "Kein Fehler", error
           

@app.route("/print", methods=["GET"] )
def print_image_route():
    global current_img
    has_error, error = has_printer_errors()

    if has_error == False:
        return render_template("print.html", img_name = current_img)
    else:
        return redirect('http://127.0.0.1:5000/error')

@app.route("/error", methods=["GET"] )
def show_error():
    has_error, error = has_printer_errors()
    if has_error == True:
        return render_template("show_error.html", error = error)
    else:
        return redirect('http://127.0.0.1:5000/print')

@app.route("/abort-job", methods=["GET"])
def abort_job():
    conn = cups.Connection()
    jobsDict = conn.getJobs()
    jobInt = list(jobsDict.keys())[0]
    try:
        conn.cancelJob(jobInt, purge_job = False)
    except Exception as E:
        print("Fehler beim JobKilL")
        print(E)
    return redirect('http://127.0.0.1:5000/preview')


if __name__ == "__main__":
    app.run(debug=True)

