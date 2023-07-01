import numpy as np
import transformacions
import math
import imutils

def calcular_distancia_media_punts(puntos):

    # Calcular la distancia media entre los puntos de una imagen
    if len(puntos) > 1:
        distancias = np.sqrt(np.sum((puntos[1:] - puntos[:-1])**2, axis=1))
        distancia_media = np.mean(distancias)
    else:
        distancia_media = 0

    return distancia_media



def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


#Funció que calula la distància del KpB amb el Kpa en B, inliers i utliers
def quality(kpsA, kpsB, matches, transf, M, L,threshold):

    #threshold=Distancia a la que cosniderem que un mach es un outlier
    
    #Calulem els KpA en les coordenades de B

    #Quan hi h una rotació
    if transf in [1,2,3]:
        kpsAenB = transformacions.transform_points_rot(kpsA, M)
    
    #Quan hi ha una translació he de restar -L en les y de kpA
    elif transf in [4,5,6]:
        kpsAenB = transformacions.transform_points_transl(kpsA, L)
    
    #Quan hi ha soroll
    elif transf in [7,8,9,10,11,12,13,14,15,16,17,18,19]:
        kpsAenB = kpsA
  
    #Litese on es guarden els kpA i kpB que hna fet match per poderlos dibuixar
    inlinersA=[]
    inlinersB=[]

    distancies=[]#Llista on guardaré les distancies entre el KpB i el Kbprojectat
    for match in matches:
        puntB_real=kpsAenB[match[1]]
        puntB=kpsB[match[0]]
        dist=euclidean_distance(puntB_real, puntB)
        distancies.append(dist)
        
        #claulo outiliers i inliers
        if dist <= threshold:
            inlinersA=inlinersA+[kpsA[match[1]]]
            inlinersB=inlinersB+[kpsB[match[0]]]
    
    #caluclo el nº de punts que tenen una distancia menor que un treshold i els guardo en l llista, cada posició de la llista correspon a una distancia de 1 a 10 pixels
    l=[]
    for threshold in [1,2,3,4,5,6,7,8,9,10]:
        p=n_punts_menors_que_d(distancies,threshold)
        l.append(p)
    
    return(inlinersA,inlinersB,l)


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
    

def esparcitat(img, points):
    #Una desviació estandard alta indica que els valors estan més dispersos, per tant hi ha més diferencia entre punts de cada quadrant i els punts estan més concentarts en una zona
    lista=punts_per_quadrant(img, points)

    media = np.mean(lista)
    prov=lista/media
    desv_std = np.std(prov)
    return desv_std


def n_punts_menors_que_d(llista, distancia):
    #calcula el percentatge distancies en una llista que son menors que un nombre
    n=0
    for d in llista:
        if d<distancia:
            n=n+1
    
    return(n/len(llista))




if __name__ == "__main__":
    import estudi_descriptors
    import cv2
    import numpy as np

    # Cargar la imagen
    image = cv2.imread("Dataset\First_Turbine_A_MID_1.png")
    image=estudi_descriptors.resize_bordes(image)
    # Obtener las dimensiones de la imagen
    points=[(130,112),(110,122),(120,122),(100,122),(432,321),(123,213),(122,223),(124,233),(123,225),(113,225),(323,245),(323,212),(300,61),(300,71),(300,81),(200,200)]
    lista=punts_per_quadrant(image, np.array(points))

