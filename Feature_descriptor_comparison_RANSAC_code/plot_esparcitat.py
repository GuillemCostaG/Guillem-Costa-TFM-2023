import cv2
import numpy as np
import transformacions

#COPIO LA FUNCIÓ DE MASURES AQUI PERQUE NO ENTENC PERQUE NO EM RETORNA LA LLISTASI FAIG IMPORT
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


def grafic_esparcitat(image,points,transf):

    #Si la meva tarndformació es una rotació la imatge estrà girada, per tant he de ficarla recta i girar els punts
    if transf==1:#si es una rotació de 2 graus
        image,M=transformacions.rotate_image(image, -2)
        points=transformacions.transform_points_rot(points, M)
    elif transf==2:#si es una rotació de 15 graus
        image,M=transformacions.rotate_image(image, -15)
        points=transformacions.transform_points_rot(points, M)
    elif transf==3:#si es una rotació de 35 graus
        image,M=transformacions.rotate_image(image, -35)
        points=transformacions.transform_points_rot(points, M)

    height, width, channels = image.shape

    quadrants = [] #Lista meb els 12 quadrats en cada un fica x,y del punt adal esquerra i la llargada i amplada del quadrat
    for i in range(3):
        for j in range(4):
            x = int(j * (width / 4))
            y = int(i * (120))+60
            w = int(width / 4)
            h = int(120)
            quadrants.append((x, y, w, h))
    if len(points)>0:
        l_punts_quadrant=punts_per_quadrant(image,np.array(points))#Lista amb els punts de cada quadrant
    else:
        return image


    # Crear una imagen transparente del mismo tamaño que la original
    overlay = image.copy()

    p_max=max(l_punts_quadrant)
    a=0
    for i in range(len(quadrants)):
        # Dibujar el rectángulo en la imagen transparente

        #Punts en el quadrant
        n_punts=l_punts_quadrant[i]

        if n_punts>0.8*p_max:
            a=1
            color=(0, 0, 255) 

        elif n_punts>0.6*p_max:
            a=1
            color=(0, 128, 255)

        elif n_punts>0.4*p_max:
            a=1
            color=(0, 255, 255) 

        elif n_punts>0.2*p_max:
            a=1
            color=(0, 255, 125)
        else:
            a=0

        #x,y del punt superior esquerra del quadrant h i w del quadrat.
        quadrat=quadrants[i]
        x=quadrat[0]
        y=quadrat[1]
        w=quadrat[2]
        h=quadrat[3]

        #Pinta el quadrant
        if a>0:
            cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)

    alpha=0.3 
    image=cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
  

    # Pintamos los cuadrantes con líneas verdes y los puntos con rojo
    for x, y, w, h in quadrants:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #for point in points:
            #if x <= point[0] < x+w and y <= point[1] < y+h:
                #cv2.circle(image, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)
    
    #Si la meva tarndformació es una rotació tornoo a girar la imatge per deixarla com estava
    if transf==1:#si es una rotació de 2 graus
        image,M=transformacions.rotate_image(image, 2)
    elif transf==2:#si es una rotació de 15 graus
        image,M=transformacions.rotate_image(image, 15)
    elif transf==3:#si es una rotació de 35 graus
        image,M=transformacions.rotate_image(image, 35)
    
    image=add_legend(image, p_max)
    
    return(image)

def add_legend(image, p_max):
    # Dibujar los cuadraditos de la leyenda
    colors = [(0, 0, 255), (0, 128, 255), (0, 255, 255), (0, 255, 125)]
    for i, color in enumerate(colors):
        x = image.shape[1] - 50
        y = 20 + i * 30
        cv2.rectangle(image, (x, y), (x+20, y+20), color, -1)

    # Dibujar los textos de la leyenda
    texts = ['+'+str(int(p_max*0.8)), '+'+str(int(p_max*0.6)), '+'+str(int(p_max*0.4)), '+'+str(int(p_max*0.2))]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    thickness = 2
    for i, text in enumerate(texts):
        x = image.shape[1] - 70
        y = 35 + i * 30
        cv2.putText(image, text, (x, y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    return image

if __name__ == "__main__":
    import estudi_descriptors
    # Cargar la imagen
    image = cv2.imread("Dataset\First_Turbine_A_MID_1.png")
    image=estudi_descriptors.resize_bordes(image)
    # Obtener las dimensiones de la imagen
    points=[(130,112),(110,122),(120,122),(100,122),(432,321),(123,213),(122,223),(124,233),(123,225),(113,225),(323,245),(323,212),(300,61),(300,71),(300,81),(200,200)]
    #points=[(360,75)]
    #image,M=transformacions.rotate_image(image, 35)
    image=grafic_esparcitat(image,points,4)

    # Mostrar la imagen con el rectángulo
    cv2.imshow("Imagen con rectángulo", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    lista=punts_per_quadrant(image, np.array(points))
    print(lista)
