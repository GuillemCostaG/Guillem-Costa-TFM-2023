import cv2
import numpy as np


def marcar_puntos(imagen, lista_puntos, color=1):
    """
    Dada una imagen y una lista de puntos, marca los puntos indicados en rojo en la imagen.
    """
    # Crea una nueva imagen basada en la original
    imagen_modificada = imagen.copy()
    
    # Define el color rojo
    if color == 1:
        color_punto = (0, 0, 255)
    elif color == 2:
        color_punto = (0, 255, 0)
    elif color == 3:
        color_punto = (255, 0, 0)

    
    # Dibuja un círculo rojo de radio 3 en cada punto de la lista
    for punto in lista_puntos:
        x, y = punto
        cv2.circle(imagen_modificada, (int(x), int(y)), 3, color_punto, -1)
    
    return imagen_modificada

def unir_matches(imagen1, imagen2, inlinersA, inlinersB):
    altura_maxima = max(imagen1.shape[0], imagen2.shape[0])

    # Crear una imagen vacía con el doble de ancho para mostrar ambas imágenes una al lado de la otra
    nueva_imagen = np.zeros((altura_maxima, imagen1.shape[1] + imagen2.shape[1], 3), dtype=np.uint8)
        
    # Copiar la primera imagen a la nueva imagen
    nueva_imagen[:imagen1.shape[0], :imagen1.shape[1]] = imagen1
        
    # Copiar la segunda imagen a la nueva imagen
    nueva_imagen[:imagen2.shape[0], imagen1.shape[1]:] = imagen2

    for match in range(len(inlinersA)): 
        punto1=inlinersA[match]
        punto2=inlinersB[match]

        punto1 = (int(punto1[0]), int(punto1[1]))
        punto2 = (int(punto2[0]), int(punto2[1]))

        # Dibujar una línea desde punto1 a punto2 en la nueva imagen
        punto1 = (punto1[0], punto1[1])
        punto2 = (punto2[0] + imagen1.shape[1], punto2[1])
        cv2.line(nueva_imagen, punto1, punto2, (0, 255, 0), thickness=1)
    return (nueva_imagen)

if __name__ == "__main__":
    image = cv2.imread("Dataset\First_Turbine_A_MID_1.png")
    #image=estudi_descriptors.resize_bordes(image)
    # Obtener las dimensiones de la imagen
    inlinersA=[(130,112),(110,122),(120,122),(100,122),(432,321),(123,213),(122,223),(124,233),(123,225),(113,225),(323,245),(323,212),(300,61),(300,71),(300,81),(200,200)]
    inlinersB=[(130,112),(110,122),(120,122),(100,122),(432,321),(123,213),(122,223),(124,233),(123,225),(113,225),(323,245),(323,212),(300,61),(300,71),(300,81),(200,200)]

    imagen1=marcar_puntos(image,inlinersA)
    imagen2=marcar_puntos(image,inlinersB)

    nueva_imagen=unir_matches(imagen1, imagen2, inlinersA, inlinersB)


    cv2.imshow("Imagen", nueva_imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()