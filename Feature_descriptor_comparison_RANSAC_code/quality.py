#Script que em permet pintar els punts reals i punts calulats en B i calcula rla qualitat

import cv2
import os
import estudi_descriptors
import numpy as np
import transformacions
import draw


# Definir la ruta de la imagen
ruta_imagenA = 'Imatges/platja1.PNG'

M=0
L=0
# Cargar la imagen utilizando cv2.imread()
imageA = cv2.imread(ruta_imagenA)
imageB, M = transformacions.rotate_image(imageA, 45)
#imageA, imageB, L = transformacions.recortar_imagen(imageA, 20)
print(M)
# Definir la lista de píxeles a marcar
(rmatch, time) = estudi_descriptors.match(imageA, imageB, 'SIFT')
lista_puntosA = rmatch['kpsA']
lista_puntosB = rmatch['kpsB']

# Llamar a la función para marcar los puntos
imagen_modificadaA = draw.marcar_puntos(imageA, lista_puntosA)
imagen_modificadaB = draw.marcar_puntos(imageB, lista_puntosB,2)

#Calcula los puntos reales de A en B
lista_puntosAenB=transformacions.transform_points_rot(lista_puntosA, M)
#lista_puntosAenB=transformacions.transform_points_transl(lista_puntosA, L)

#Marca los puntos de A en B
imagen_modificadaBA = draw.marcar_puntos(imagen_modificadaB, lista_puntosAenB)

#calula la quality
dist=estudi_descriptors.quality(lista_puntosA, lista_puntosB, rmatch['matches'], 1, M, L)
#dist=estudi_descriptors.quality(lista_puntosA, lista_puntosB, rmatch['matches'], 2, M, L)
print(dist)

# Crear la carpeta "results" si no existe
if not os.path.exists("results"):
    os.mkdir("results")

# Guardar la imagen resultante en la carpeta "results"
cv2.imwrite("results/mi_imagen_modificadaA.jpg", imagen_modificadaA)
cv2.imwrite("results/mi_imagen_modificadaB.jpg", imagen_modificadaB)
cv2.imwrite("results/mi_imagen_modificadaBA.jpg", imagen_modificadaBA)



