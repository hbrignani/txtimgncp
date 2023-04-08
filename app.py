from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, redirect, url_for, render_template
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST' and 'image' in request.files:
        # Obtener archivo de imagen subido y cargar la imagen con PIL
        image_file = request.files['image']
        image = Image.open(image_file)

        # Cargar la imagen del logo y obtener sus dimensiones
        logo_path = 'logo.png'
        logo = Image.open(logo_path)
        logo_width, logo_height = logo.size

        # Agregar el logo en la esquina superior derecha con un margen de 24 píxeles
        margin = 24
        image.paste(logo, (image.width - logo_width - margin, margin), logo)

        # Agregar el título en el tercio inferior izquierdo
        text = request.form.get('text')
        text_margin = 40
        text_size = 30
        text_font = ImageFont.truetype('arial.ttf', text_size)
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(text, font=text_font)
        text_position = (text_margin, image.height - text_margin - text_height)
        draw.text(text_position, text, font=text_font, fill=(255, 255, 255, 255))

        # Cambiar tamaño de la imagen final a 1080x1080
        size = (1080, 1080)
        image.thumbnail(size, Image.ANTIALIAS)

        # Guardar la imagen final con un nombre único en la carpeta de subidas
        upload_dir = 'uploads/'
        filename = str(uuid.uuid4()) + '.jpg'
        image.save(os.path.join(upload_dir, filename), 'JPEG')

        # Redireccionar a la página que muestra la imagen subida
        return redirect(url_for('view_image', filename=filename))

    return render_template('index.html')

@app.route('/uploads/<filename>')
def view_image(filename):
    return render_template('view.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
