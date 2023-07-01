import numpy as np
import math
import estudi_descriptors

def dist_matrix(H1,H2):
#ALGORITME NCC
# Definir las dos matrices
    a = np.array(H1)
    b = np.array(H2)

    # Calcular la media de cada matriz
    mean_a = np.mean(a)
    mean_b = np.mean(b)

    # Calcular la desviación estándar de cada matriz
    std_a = np.std(a)
    std_b = np.std(b)

    # Normalizar las matrices
    a_norm = (a - mean_a) / std_a
    b_norm = (b - mean_b) / std_b

    # Calcular la NCC
    ncc = np.sum(a_norm * b_norm) / (a.shape[0] * a.shape[1])

    return ncc


def compare_H(H1,transf):
    if transf ==1:
        angle_graus=2
        angle_radians=math.radians(angle_graus)
        H2=[[math.cos(angle_radians),math.sin(angle_radians),0],
            [-math.sin(angle_radians),math.cos(angle_radians),0],
            [0,0,1]]
    
    if transf ==2:
        angle_graus=15
        angle_radians=math.radians(angle_graus)
        H2=[[math.cos(angle_radians),math.sin(angle_radians),0],
            [-math.sin(angle_radians),math.cos(angle_radians),0],
            [0,0,1]]    
            
    if transf ==3:
        angle_graus=35
        angle_radians=math.radians(angle_graus)
        H2=[[math.cos(angle_radians),math.sin(angle_radians),0],
            [-math.sin(angle_radians),math.cos(angle_radians),0],
            [0,0,1]]
        
    if transf ==4:
        pixels=25
        H2=[[1,0,pixels],
            [0,1,0],
            [0,0,1]]
         
    if transf ==5:
        pixels=53
        H2=[[1,0,pixels],
            [0,1,0],
            [0,0,1]]   
        
    if transf ==6:
        pixels=75
        H2=[[1,0,pixels],
            [0,1,0],
            [0,0,1]]    
    
    if transf in [7,8,9,10,11,12,13,14,15,16,17,18,19]:
        H2=[[1,0,0],
            [0,1,0],
            [0,0,1]]   
    

    return(dist_matrix(H1,H2))







if __name__ == "__main__":

    import cv2
    import numpy as np

    def procesar_imagen_rot(punto1,punto2):
        # Cargar la imagen
        imagen = cv2.imread('Dataset\First_Turbine_A_MID_1.png')
        imagen=estudi_descriptors.resize_bordes(imagen)

        # Rotar la imagen
        angulo_rotacion = 35
        filas, columnas = imagen.shape[:2]
        matriz_rotacion = cv2.getRotationMatrix2D((columnas/2, filas/2), angulo_rotacion, 1)
        imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (columnas, filas))


        # Dibujar puntos en las imágenes
        color = (0, 255, 0)  # Color verde
        grosor = 5
        radio = 1
        cv2.circle(imagen, punto1, radio, color, grosor)
        cv2.circle(imagen_rotada, punto2, radio, color, grosor)

        # Crear una imagen nueva con ambas imágenes
        imagen_completa = np.hstack((imagen, imagen_rotada))

        # Mostrar la imagen completa
        cv2.imshow('Imagen Completa', imagen_completa)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def procesar_imagen_id(punto1,punto2):
        # Cargar la imagen
        imagen = cv2.imread('Dataset\First_Turbine_A_MID_1.png')
        imagen=estudi_descriptors.resize_bordes(imagen)

        # Rotar la imagen
        imagen_modificada = imagen.copy()   


        # Dibujar puntos en las imágenes
        color = (0, 255, 0)  # Color verde
        grosor = 5
        radio = 1
        cv2.circle(imagen, punto1, radio, color, grosor)
        cv2.circle(imagen_modificada, punto2, radio, color, grosor)

        # Crear una imagen nueva con ambas imágenes
        imagen_completa = np.hstack((imagen, imagen_modificada))

        # Mostrar la imagen completa
        cv2.imshow('Imagen Completa', imagen_completa)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def pintar_puntos(puntosA,puntosB):
        # Cargar la imagen
        imagen = cv2.imread('Dataset\First_Turbine_A_MID_1.png')
        imagen=estudi_descriptors.resize_bordes(imagen)

        # Rotar la imagen
        angulo_rotacion = 35
        filas, columnas = imagen.shape[:2]
        matriz_rotacion = cv2.getRotationMatrix2D((columnas/2, filas/2), angulo_rotacion, 1)
        imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (columnas, filas))

        # Dibujar puntos en las imágenes
        color = (0, 255, 0)  # Color verde
        grosor = 5
        radio = 1

        for punto1 in puntosA:
            punto1=(int(punto1[0]), int(punto1[1]))
            cv2.circle(imagen, punto1, radio, color, grosor)
        
        for punto2 in puntosB:
            punto2=(int(punto2[0]), int(punto2[1]))
            cv2.circle(imagen_rotada, punto2, radio, color, grosor)

        # Crear una imagen nueva con ambas imágenes
        imagen_completa = np.hstack((imagen, imagen_rotada))

        # Mostrar la imagen completa
        cv2.imshow('Imagen Completa', imagen_completa)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    import numpy as np
    angle_radians=math.radians(35)
    angle_radians

    H1=[[math.cos(angle_radians),math.sin(angle_radians),0],
    [-math.sin(angle_radians),math.cos(angle_radians),0]]
    print(H1)

    H2=[[1,0,0],[0,1,0],[1,0,1]]
    
    #Obtinguda de inferencia1 rotacio
    H3=[[ 8.23873042e-01,  5.79321842e-01, -8.12695574e+01],[-5.73790210e-01 , 8.26581556e-01  ,2.25784934e+02]]
 
    
    #Obtinguda de inferencia1 Identitat
    H4=[[ 1.00000000e+00, -6.81903726e-14,  1.73282014e-11],
    [-6.54820579e-15,  1.00000000e+00,  7.77799947e-12]]

    #M obtinguda de la funcio que fa rotar 35
    H5=[[  0.81915204,   0.57357644, -79.7869989 ],
        [ -0.57357644,   0.81915204, 226.947969  ]]
    #Translacio
    H7=[[ 1.01200210e+00, -1.76810934e-03 , 7.28684959e+01],[ 8.12173456e-04 , 1.00358692e+00 ,-2.56533377e-01]]
 
    # Definir el vector de 1 columna y 2 filas
    P1 = np.array([[200], [215],[1] ])

    H=np.array(H1)
    # Realizar la multiplicación
    #P2= H.dot(P1)
    P2 = np.dot(H, P1)

    P1 = (int(P1[0]), int(P1[1]))
    P2 = (int(P2[0]), int(P2[1]))

    # Llamar a la función
    #procesar_imagen_rot(P1,P2)

    #procesar_imagen_id(P1,P2)


    points=[[548.   ,     60.      ],
 [543.,        62.      ],
 [553.,        65.      ],
 [551. ,       66.      ],
 [339. ,       96.      ],
 [ 71. ,      265.      ],
 [376. ,      419.      ],
 [400. ,      419.      ],
 [417. ,      419.      ],
 [421. ,      419.      ],
 [547.2 ,      60.000004],
 [ 70.8 ,     265.2     ],
 [375.6  ,    418.80002 ],
 [399.6  ,    418.80002 ],
 [416.40002 , 418.80002 ],
 [420.00003 , 418.80002 ],
 [545.76   ,   60.480003],
 [ 70.560005, 264.96002 ],
 [377.28003,  417.6     ],
 [400.32   ,  417.6     ],
 [416.16  ,   417.6     ],
 [420.48  ,   417.6     ],
 [546.04803,   60.480007],
 [378.43204 , 418.17603 ],
 [400.89603,  418.17603 ],
 [416.44803 , 418.17603 ],
 [515.9782 ,  279.4882  ]]

    points2=[(403, -38), (400, -33), (410, -36), (409, -35), (252, 111), (130, 403), (468, 354), (488, 340), (502, 330), (505, 328), (402, -37), (130, 403), (468, 354), (487, 340), (501, 331), (504, 329), (401, -36), (129, 403), (468, 352), (487, 339), (500, 330), (504, 327), (402, -36), (470, 352), (488, 339), (501, 330), (503, 159)]

    M=np.array([[  0.81915204 ,  0.57357644, -79.7869989 ],[ -0.57357644,   0.81915204, 226.947969  ]])

    import transformacions

    points2=transformacions.transform_points_rot(points,np.array(H3))

    pintar_puntos(points,points2)

    H6=[[1,0,10],[0,1.0001,0]]
    
    imagen = cv2.imread('Dataset\First_Turbine_A_MID_1.png')
    imagen=estudi_descriptors.resize_bordes(imagen)
    imatge_transformada=cv2.warpAffine(imagen, np.array(H3), (640, 480))

    out = cv2.hconcat([imagen,imatge_transformada])
    cv2.imshow('a2',out)
    cv2.waitKey(0)

    #rotacio 2 graus
    Hreal=[[ 0.99939083,  0.0348995,  -8.18094385],[-0.0348995 ,  0.99939083 ,11.31404046]]
    H_experimental=[[ 1.00061611e+00,  3.56672356e-02, -8.51114521e+00],[-3.48450120e-02 , 1.00169559e+00 , 1.09402339e+01]]

    #rotacio 15 graus
    Hreal=[[  0.96592583,   0.25881905, -51.21283524],[ -0.25881905,   0.96592583,  90.99989612]]
    H_experimental=[[ 9.68267529e-01,  2.62114597e-01, -5.23202638e+01],[-2.58892817e-01 , 9.69530779e-01,  9.05002375e+01]]