import os
import cv2
import imutils
import numpy as np


def resize_bordes(img):
    #Funció que fa la imatge (480, 640, 3). Fica una bordes negres a la imatge adal i abaix  
    img=imutils.resize(img, width=640)
    new_img=img

    #Fica bordes negres a la imatge perque fagi 480 en la y.
    h, w, c = img.shape


    # calcular la cantidad de píxeles que se deben agregar en los lados
    border_width = int((480 - h) / 2)

    # crear una matriz de ceros del tamaño deseado
    new_img = np.zeros((480, w, c), dtype=np.uint8)

    # agregar los píxeles de la imagen original en el centro de la nueva matriz
    new_img[border_width:border_width+h, :, :] = img    
    
    return new_img


# nombre del archivo de video
video_file = "30s.mp4"

# crear la carpeta rgb si no existe
if not os.path.exists("rgb"):
    os.makedirs("rgb")

# abrir el archivo de video
cap = cv2.VideoCapture(video_file)

# obtener la tasa de fotogramas (FPS) y la duración del video
fps = cap.get(cv2.CAP_PROP_FPS)
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frames / fps

# crear el archivo de texto y escribir las primeras líneas
with open("rgb.txt", "w") as f:
    f.write("# color images\n")
    f.write(f"# file: '{video_file}'\n")
    f.write("# timestamp filename\n")

# iterar sobre los fotogramas y guardar las imágenes
for i in range(frames):
    # leer el fotograma actual
    ret, frame = cap.read()
    if not ret:
        break
    
    # calcular el tiempo del fotograma actual
    timestamp = round(i / fps, 6)
    
    # guardar la imagen
    filename = f"rgb/{timestamp:.6f}.png"
    frame=resize_bordes(frame)
    cv2.imwrite(filename, frame)
    
    # escribir la información en el archivo de texto
    with open("rgb.txt", "a") as f:
        f.write(f"{timestamp:.6f} rgb/{timestamp:.6f}.png\n")
    
# liberar los recursos y cerrar los archivos
cap.release()