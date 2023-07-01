import numpy as np
import cv2
import estudi_descriptors

def punts_per_quadrant(img, points):
    #Calcula el nº de punts en cada quadrant de la image i retorna una llista on cada valor són els punts en cada quadrant
    # Dividir la imagen en 12 cuadrantes
    height, width, _ = img.shape
    h_unit = (height - 120) // 3
    w_unit = width // 4
 
    # Calcular el número de puntos en cada cuadrante
    counts = []
    for i in range(3):
        for j in range(4):
            y_min = 60 + i * h_unit
            y_max = 60 + (i + 1) * h_unit
            x_min = j * w_unit
            x_max = (j + 1) * w_unit
            quadrant_mask = (points[:, 0] >= x_min) & (points[:, 0] < x_max) & \
                            (points[:, 1] >= y_min) & (points[:, 1] < y_max)
            count = np.sum(quadrant_mask)
            counts.append(count)

    return counts

if __name__ == "__main__":
    image = cv2.imread("Dataset\First_Turbine_A_MID_1.png")
    image=estudi_descriptors.resize_bordes(image)
    # Obtener las dimensiones de la imagen
    points=np.array([(10,299)])

    a=punts_per_quadrant(image, points)
    print(a)