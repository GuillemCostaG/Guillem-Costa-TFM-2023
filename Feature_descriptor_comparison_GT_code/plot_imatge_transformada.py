import cv2
import numpy as np
#import estudi_descriptors

def draw_imatge_transformada(imatgeA, imatgeB, H):
 
    imatge_transformada=cv2.warpAffine(imatgeA, np.array(H[:2]), (640, 480))

    out = cv2.hconcat([imatgeB,imatge_transformada])

    return(out)


if __name__ == "__main__":
    imagen = cv2.imread('Dataset\First_Turbine_A_MID_1.png')
    #imagen=estudi_descriptors.resize_bordes(imagen)

    # Rotar la imagen
    angulo_rotacion = 35
    filas, columnas = imagen.shape[:2]
    matriz_rotacion = cv2.getRotationMatrix2D((columnas/2, filas/2), angulo_rotacion, 1)
    imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (columnas, filas))

    H_inliners=[[  0.81915204,   0.57357644, -79.7869989 ],
        [ -0.57357644,   0.81915204, 226.947969  ]]

    out=draw_imatge_transformada(imagen, imagen_rotada, H_inliners)

    cv2.imshow('a2',out)
    cv2.waitKey(0)
