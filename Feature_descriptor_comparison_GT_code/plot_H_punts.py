import transformacions
import numpy as np
import cv2
import matplotlib.pyplot as plt
#import estudi_descriptors

def H_transf(transf):

    if transf ==1:
        H_teorica=[[ 0.99939083,  0.0348995,  -8.18094385],[-0.0348995 ,  0.99939083 ,11.31404046]]
    
    if transf ==2:
        H_teorica=[[  0.96592583,   0.25881905, -51.21283524],[ -0.25881905,   0.96592583,  90.99989612]]
            
    if transf ==3:
        H_teorica=[[  0.81915204,   0.57357644, -79.7869989 ],
        [ -0.57357644,   0.81915204, 226.947969  ]]
        
    if transf ==4:
        pixels=25
        H_teorica=[[1,0,pixels],
            [0,1,0]]
         
    if transf ==5:
        pixels=53
        H_teorica=[[1,0,pixels],
            [0,1,0]]   
        
    if transf ==6:
        pixels=75
        H_teorica=[[1,0,pixels],
            [0,1,0]]    
    
    if transf in [7,8,9,10,11,12,13,14,15,16,17,18,19]:
        H_teorica=[[1.00001,0,0],
            [0,1,0]] 
        
    return(H_teorica)


def pintar_puntos_H(puntosA,puntosB, puntosC, imagenA, imagenB):
        # Cargar la imagen
        # Dibujar puntos en las imágenes
        color = (0, 255, 0)  # Color verde
        grosor = 2
        radio = 1

        for punto1 in puntosA:
            punto1=(int(punto1[0]), int(punto1[1]))
            cv2.circle(imagenA, punto1, radio, color, grosor)
        
        for punto2 in puntosC:
            punto2=(int(punto2[0]), int(punto2[1]))
            cv2.circle(imagenB, punto2, radio, color, grosor)
        
        color = (0, 0, 255)  # Color rojo
        grosor = 1
        radio = 2

        for punto2 in puntosB:
            punto2=(int(punto2[0]), int(punto2[1]))
            cv2.circle(imagenB, punto2, radio, color, grosor)

        # Crear una imagen nueva con ambas imágenes
        imagen_completa = np.hstack((imagenA, imagenB))

        return(imagen_completa)



def generate_random_points(image_height, image_width, num_points):
    valid_range_y = (60, 420)  # Rango válido para la coordenada y

    points = []
    while len(points) < num_points:
        point = np.random.rand(1, 2)
        point[:, 0] *= image_width  # Escalar el valor x al rango de ancho de la imagen

        # Escalar el valor y al rango válido (60-420)
        point[:, 1] = point[:, 1] * (valid_range_y[1] - valid_range_y[0]) + valid_range_y[0]

        # Verificar si el punto cumple con las restricciones y agregarlo a la lista
        if point[:, 1] >= valid_range_y[0] and point[:, 1] <= valid_range_y[1]:
            points.append(point)

    points = np.concatenate(points, axis=0)
    return points

def n_punts_menors_que_d(llista, distancia):
    #calcula el percentatge distancies en una llista que son menors que un nombre
    n=0
    for d in llista:
        if d<distancia:
            n=n+1
    
    return(n/len(llista))


def distancia_puntos(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def distancia_punts(points_H_teorica, points_H_real):
    #clcula la mitja de la distancia que hi ha entre els punts calculats amb la H teorica i H real
    distances = []
    for i in range(len(points_H_teorica)):
        distance = distancia_puntos(points_H_teorica[i], points_H_real[i])
        distances.append(distance)
    #print(distances)

    #caluclo el nº de punts que tenen una distancia menor que un treshold i els guardo en l llista, cada posició de la llista correspon a una distancia de 1 a 10 pixels
    l=[]
    for threshold in [1,2,3,4,5,6,7,8,9,10]:
        p=n_punts_menors_que_d(distances,threshold)
        l.append(p)
    
    suma=sum(distances)
    mitja=suma/len(distances)

    return (mitja,l) #lista amb el % de parelles de punts que estan a una distancia emnor de [1,2,3,4,5,6,7,8,9] pixels.
    
    

def plot_H_random_points(imagenA, imagenB, H_inliners, transf):
    random_points = generate_random_points(480, 640, 200)
    H_real=np.array(H_inliners)
    H_teorica=H_transf(transf)
    
    points_H_teorica=transformacions.transform_points_rot(random_points,np.array(H_teorica))
    points_H_real=transformacions.transform_points_rot(random_points,np.array(H_real))

    #imagen_completa=pintar_puntos_H(random_points[:20],points_H_real[:20], points_H_teorica[:20],imagenA, imagenB)

    mitja_d, p_punts_distancia=distancia_punts(points_H_teorica, points_H_real) #llista amb distancies entre punts

    return(p_punts_distancia, mitja_d)
    



if __name__ == "__main__":
    imagen = cv2.imread('Dataset\First_Turbine_A_MID_1.png')
    #imagen=estudi_descriptors.resize_bordes(imagen)

    # Rotar la imagen
    angulo_rotacion = 35
    filas, columnas = imagen.shape[:2]
    matriz_rotacion = cv2.getRotationMatrix2D((columnas/2, filas/2), angulo_rotacion, 1)
    imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (columnas, filas))

    H_inliners=[[ 8.23873042e-01,  5.79321842e-01, -8.12695574e+01],[-5.73790210e-01 , 8.26581556e-01  ,2.25784934e+02]]

    imagen_completa, mitja_distancia, mitja_d =plot_H_random_points(imagen, imagen_rotada, H_inliners, 3)

    print('distància mitja = '+str(mitja_distancia))

    # Mostrar la imagen completa
    cv2.imshow('Imagen Completa', imagen_completa)
    cv2.waitKey(0)
    cv2.destroyAllWindows()