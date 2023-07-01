import cv2
import numpy as np

# Listas de puntos correspondientes en las dos imágenes
pts1 = np.array([(10, 20), (30, 40), (50, 60), (70, 80)])
pts2 = np.array([(10, 20), (30, 40), (50, 60), (70, 80)])

# Calcula la homografía sin utilizar RANSAC
H, _ = cv2.findHomography(pts1, pts2, 0)

print(H)