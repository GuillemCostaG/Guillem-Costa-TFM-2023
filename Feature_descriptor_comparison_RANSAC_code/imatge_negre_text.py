from PIL import Image, ImageDraw, ImageFont
import numpy as np

def crear_imagen_con_texto(texto, ancho, alto):
    # Crea una imagen en negro con las dimensiones especificadas
    imagen = Image.new("RGB", (ancho, alto), color=(0, 0, 0))

    return np.array(imagen)

