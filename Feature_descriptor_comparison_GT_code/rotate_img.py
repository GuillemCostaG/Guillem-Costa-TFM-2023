import cv2
import plot_esparcitat

def rotate_image(image, angle):
    # Obtener la altura y anchura de la imagen
    height, width = image.shape[:2]
    
    # Calcular el centro de la imagen
    center = (width / 2, height / 2)
    
    # Definir la matriz de transformación de afinidad
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Aplicar la transformación de afinidad a la imagen
    rotated = cv2.warpAffine(image, M, (width, height))

    
    return(rotated,M)

if __name__ == "__main__":
    import estudi_descriptors
    # Cargar la imagen
    image = cv2.imread("Dataset\First_Turbine_A_MID_1.png")
    image=estudi_descriptors.resize_bordes(image)
    # Obtener las dimensiones de la imagen
    points=[(130,112),(110,122),(120,122),(100,122),(432,321),(123,213),(122,223),(124,233),(123,225),(113,225),(323,245),(323,212),(300,61),(300,71),(300,81),(200,200)]
    # Mostrar la imagen con el rectángulo
    image,M=rotate_image(image, 20)

    image,M=rotate_image(image, -20)

    image=plot_esparcitat.grafic_esparcitat(image,points)
    
    # Mostrar la imagen con el rectángulo
    cv2.imshow("Imagen con rectángulo", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image,M=rotate_image(image, 20)
    # Mostrar la imagen con el rectángulo
    cv2.imshow("Imagen con rectángulo", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

