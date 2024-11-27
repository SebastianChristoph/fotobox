from PIL import Image, ImageDraw, ImageFont

def resize_img(img_path):
    print("start resizing")
    with Image.open(img_path) as img:
        # Aktuelle Größe des Bildes holen
        width, height = img.size
        print(f"Alt: Breite {width} ; Höhe {height}")
        # Neue Größe berechnen (50% der aktuellen Größe)
        new_size = (width //3, height //3)
        
        # Bild skalieren
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Bild am selben Pfad speichern (überschreiben)
        
        img_resized.save(img_path)

        width, height = img_resized.size
        print(f"Neu: Breite {width} ; Höhe {height}")


        print("saved resized image")
    


def add_text_to_image(img_path, text, font):
    print("start adding text to image")

    font_path = "static/fonts/" 
    font_size_factor = 0.05
    y_versatz = 15
    y_versatz_rect = 30

    # Bestimmen der Schriftart basierend auf der Eingabe
    if font == "Boho":
        font_path += "Boho.otf"
        y_versatz = 25
        y_versatz_rect = 20
        font_size_factor = 0.07
    elif font == "Edel":
        y_versatz_rect = 35
        y_versatz = 15
        font_path += "Edel.otf"
    elif font == "Love":
        font_path += "Love.otf"
        y_versatz = 25
        y_versatz_rect = 5
        font_size_factor = 0.06
    else:
        y_versatz_rect = 0
        y_versatz = 30
        font_path += "Normal.ttf"

    # Bild öffnen und sicherstellen, dass es im RGBA-Modus ist
    with Image.open(img_path).convert("RGBA") as img:
        breite, hoehe = img.size
        draw = ImageDraw.Draw(img)
        
        # Schriftart und Größe festlegen
        font_size = int(breite * font_size_factor)  # Schriftgröße relativ zur Bildbreite
        try:
            font = ImageFont.truetype(font_path, font_size)  # Versuch, eine benutzerdefinierte Schrift zu verwenden
        except IOError as e:
            print(f"Error loading font {font_path}: {e}")
            font = ImageFont.load_default()  # Fallback auf Standardschrift, falls benutzerdefinierte Schrift nicht verfügbar ist
        
        # Textgröße berechnen
        bbox = draw.textbbox((0, 0), text, font=font)  # Erhalte Bounding-Box
        text_breite = bbox[2] - bbox[0]  # Berechne Breite
        text_hoehe = bbox[3] - bbox[1]  # Berechne Höhe
        
        # Rechteckgröße und Position
        rechteck_breite = text_breite + 40  # Puffer für das Rechteck
        rechteck_hoehe = text_hoehe + 50
        x_rechteck = (breite - rechteck_breite) // 2
        y_rechteck = int(hoehe * 0.85)
        
        # Erstelle ein transparentes Overlay-Bild
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))  # Transparentes Bild

        # Rechteckfarbe (halbtransparentes Schwarz)
        eckenradius = 15
        overlay_color = (0, 0, 0, 150)  # Schwarz mit 150/255 Transparenz
        overlay_draw = ImageDraw.Draw(overlay)

        # Rechteck mit abgerundeten Ecken (semi-transparent) auf Overlay zeichnen
        overlay_draw.rounded_rectangle(
            [x_rechteck, y_rechteck - y_versatz_rect, x_rechteck + rechteck_breite, y_rechteck + rechteck_hoehe - y_versatz_rect],
            radius=eckenradius,
            fill=overlay_color
        )
        
        # Füge das Overlay mit dem Rechteck auf das Originalbild hinzu
        img_with_overlay = Image.alpha_composite(img.convert("RGBA"), overlay)

        # Text auf das Bild mit dem Overlay zeichnen
        draw = ImageDraw.Draw(img_with_overlay)
        text_x = x_rechteck + (rechteck_breite - text_breite) // 2
        text_y = y_rechteck + (rechteck_hoehe - text_hoehe) // 2
        text_color = (255, 255, 255, 255)  # Weißer Text ohne Transparenz
        draw.text((text_x, text_y - y_versatz), text, font=font, fill=text_color)
        
        # Umwandlung zurück zu RGB für JPG-Speicherung
        img_rgb = img_with_overlay.convert("RGB")

        # Speichern als JPEG
        img_rgb.save(img_path)
        print("image with text saved")
