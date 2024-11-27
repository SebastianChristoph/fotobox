from picamera2 import Picamera2, Preview
from PyQt5.QtWidgets import QApplication, QWidget

def start_cam():
    global picam2  # Make picam2 global to access it within the function
    print("start preview")
    picam2 = Picamera2()  # Initialize camera inside the function
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    print("preview started")

def stop_cam():
    global picam2
    picam2.stop_preview()
    print("cam preview stopped")
    picam2.stop()
    print("cam stopped")
    picam2.close()  # Add this line to properly release the camera

def reset_cam():
    picam2 = Picamera2()  # Initialize camera inside the function
    picam2.start()
    picam2.stop()
    picam2.close()
    print("picam released")

#reset_cam()