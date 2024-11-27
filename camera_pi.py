import time
import threading
import io
from picamera2 import Picamera2, Preview


class Camera(object):
    thread = None  # Hintergrund-Thread, der Bilder von der Kamera liest
    frame = None  # Das aktuelle Bild wird hier vom Hintergrund-Thread gespeichert
    last_access = 0  # Zeitpunkt des letzten Zugriffs des Clients auf die Kamera

    def initialize(self):
        if Camera.thread is None:
            # Startet den Hintergrund-Frame-Thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # Warten, bis Frames verfügbar sind
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        # Initialisieren der Kamera mit Picamera2
        picam2 = Picamera2()
        picam2.configure(picam2.create_still_configuration())

        # Kamera aufwärmen
        time.sleep(1)

        # Wenn man eine Vorschau möchte, kann man sie hier starten
        picam2.start_preview(Preview.QTGL)

        # Capture-Loop (kontinuierliche Aufnahme von Bildern)
        while True:
            # Bild erfassen
            frame = picam2.capture_array()  # Gibt ein numpy-Array zurück

            # Umwandeln des numpy-Arrays in Bytes
            cls.frame = frame.tobytes()

            # Wenn in den letzten 10 Sekunden kein Client auf die Kamera zugegriffen hat, stoppe den Thread
            if time.time() - cls.last_access > 10:
                break

        cls.thread = None
