import cv2
import numpy as np
import random
import estudi_descriptors

# Leer imagen
img = cv2.imread('Imatges/transl1.PNG')

def pols(img):
    # Generar una imagen en negro del mismo tamaño que la original
    lines_img = np.zeros_like(img)

    # Configurar parámetros de las líneas
    num_lines = 20
    angle_range = range(-45, 45)

    # Generar líneas aleatorias
    for i in range(num_lines):
        # Escoger punto de inicio y longitud de la línea
        start_point = (random.randint(0, img.shape[1]), random.randint(0, img.shape[0]))
        length = random.randint(20, 300)

        # Calcular punto final de la línea a partir del ángulo y la longitud
        angle = random.choice(angle_range)
        end_point = (int(start_point[0] + length * np.sin(np.deg2rad(angle))),
                 int(start_point[1] + length * np.cos(np.deg2rad(angle))))

        # Dibujar la línea en la imagen en negro
        cv2.line(lines_img, start_point, end_point, (73, 72, 68), thickness=6)

    # Sumar las líneas a la imagen original
    result = cv2.add(img, lines_img)
    return(result)


result=pols(img)

result=estudi_descriptors.resize_bordes(result)

# Mostrar imagen resultante
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()