from PIL import Image, ImageDraw, ImageFont

def resize_img(img_path):
    print("start resizing")
    with Image.open(img_path) as img:
        # Aktuelle Größe des Bildes holen
        width, height = img.size
        # Neue Größe berechnen (50% der aktuellen Größe)
        new_size = (width // 2, height // 2)
        
        # Bild skalieren
        img_resized = img.resize(new_size, Image.ANTIALIAS)
        
        # Bild am selben Pfad speichern (überschreiben)
        img_resized.save(img_path)
        print("saved resized image")
    

def add_text_to_image(img_path, text, font):
    print("start adding text to image")

    font_path = "static/fonts/" 
    font_size_factor = 0.05

    if font == "Boho":
        font_path += "Boho.otf"
        font_size_factor = 0.1
    elif font == "Edel":
        font_path += "Edel.otf"
    elif font == "Love":
        font_path += "Love.otf"
        font_size_factor = 0.1
    else:
        font_path += "Normal.ttf"



    with Image.open(img_path) as img:
        # Bildgröße
        breite, hoehe = img.size
        draw = ImageDraw.Draw(img, "RGBA")
        
        # Schriftart und Größe festlegen (Standardschrift)
        font_size = int(breite * font_size_factor)  # Schriftgröße relativ zur Bildbreite
        try:
            font = ImageFont.truetype(font_path, font_size)  # Versuch, eine Systemschrift zu verwenden
        except IOError:
            print("Error in choosing font")
            font = ImageFont.load_default()  # Fallback auf Standardschrift, falls Arial nicht verfügbar ist
        
        # Textgröße berechnen
        text_breite, text_hoehe = draw.textsize(text, font=font)
        
        # Position des Rechtecks (ca. 70% der Bildhöhe)
        rechteck_breite = text_breite + 40  # Puffer für das Rechteck
        rechteck_hoehe = text_hoehe + 20
        x_rechteck = (breite - rechteck_breite) // 2
        y_rechteck = int(hoehe * 0.85)
        
        # Rechteck mit abgerundeten Ecken zeichnen (halbtransparentes Schwarz)
        eckenradius = 15
        overlay_color = (0, 0, 0, 150)  # Schwarz mit 150/255 Transparenz
        draw.rounded_rectangle(
            [x_rechteck, y_rechteck, x_rechteck + rechteck_breite, y_rechteck + rechteck_hoehe],
            radius=eckenradius,
            fill=overlay_color
        )
        
        # Text auf dem Rechteck zentrieren
        text_x = x_rechteck + (rechteck_breite - text_breite) // 2
        text_y = y_rechteck + (rechteck_hoehe - text_hoehe) // 2
        text_color = (255, 255, 255)  # Weißer Text
        draw.text((text_x, text_y), text, font=font, fill=text_color)
        
        # Bild speichern und Original überschreiben
        img.save(img_path)
        print("image with text saved")
