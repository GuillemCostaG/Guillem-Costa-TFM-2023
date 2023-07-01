import cv2
import numpy as np
import imutils
import random

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


def transform_points_rot(point_list, M):
    #Funcióq ue em calula la posició dels meus punts després de fer una rotació amb matriu de rotació M 
    new_point_list = []
    for point in point_list:
        # Agregar una columna de 1 a la coordenada del punto para convertirla en un vector homogéneo
        homog_point = np.array([point[0], point[1], 1])
        # Aplicar la matriz de transformación a la coordenada del punto
        new_homog_point = M.dot(homog_point)
        # Convertir el vector homogéneo de nuevo a una coordenada de punto
        new_point = (int(new_homog_point[0]), int(new_homog_point[1]))
        new_point_list.append(new_point)
    return new_point_list




def recortar_imagen(imagen, percentatge_trasl):
    #Funció que em retorna la foto desp´res d'haver-se trslladat L
    altura, anchura = imagen.shape[:2]
    recorte = int(percentatge_trasl / 100.0 * anchura)

    # Recortar columnas de la izquierda
    img_izquierda = imagen[:, recorte:]

    # Recortar columnas de la derecha
    img_derecha = imagen[:, :-recorte]

    return img_izquierda, img_derecha, recorte


def transform_points_transl(point_list, L):
    #Funcióq ue em calula la posició dels meus punts després de fer una translació amb distancia L  
          
    kpsAenB =[]

    for punto in point_list:
        # Restamos L a la coordenada y
        y_nuevo = punto[1]
        # Mantenemos la misma coordenada y
        x_nuevo = punto[0] +L
        # Creamos un nuevo punto con las coordenadas actualizadas
        nuevo_punto = [x_nuevo, y_nuevo]
        # Agregamos el nuevo punto a la lista de nuevos puntos
        kpsAenB.append(nuevo_punto)
    
    return(kpsAenB)


def add_gaussian_noise(img, mean, std):
    noise = np.random.normal(loc=mean, scale=std, size=img.shape[:2])
    noisy_img = np.copy(img)
    for i in [0,1,2]:
        noisy_img[:,:,i] = np.clip(img[:,:,i] + noise, 0, 255).astype(np.uint8)
    return noisy_img


def canvi_ilum(img, d):
    clipped_image = np.copy(img)
    kernel = np.ones((clipped_image.shape[0], clipped_image.shape[1]), np.float32) * d
    for i in range(3):
        clipped_image[:, :, i] = np.clip(clipped_image[:, :, i] + kernel, 0, 255)
    
    return clipped_image


def pols(img,num_lines):
    # Generar una imagen en negro del mismo tamaño que la original
    lines_img = np.zeros_like(img)

    # Configurar parámetros de las líneas
    angle_range = range(-90, 90)

    # Generar líneas aleatorias
    for i in range(num_lines):
        # Escoger punto de inicio y longitud de la línea
        start_point = (random.randint(0, img.shape[1]), random.randint(0, img.shape[0]))
        length = random.randint(20, 900)

        # Calcular punto final de la línea a partir del ángulo y la longitud
        angle = random.choice(angle_range)
        end_point = (int(start_point[0] + length * np.sin(np.deg2rad(angle))),
                 int(start_point[1] + length * np.cos(np.deg2rad(angle))))

        # Dibujar la línea en la imagen en negro
        cv2.line(lines_img, start_point, end_point, (73, 72, 68), thickness=6)

    # Sumar las líneas a la imagen original
    result = cv2.add(img, lines_img)

    return(result)

def blurring(img,tamany_filtre):
    img_blur=cv2.blur(img, (tamany_filtre , tamany_filtre)) #Filtre pasa-Baixos
    #imatgeB = cv2.GaussianBlur(image, (5 , 5), 0) #Filtre gausià
    
    return img_blur

def especularitat(img,n):
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización para crear máscara binaria
    thresh = cv2.threshold(gray, n, 255, cv2.THRESH_BINARY)[1]

    nova_img = np.copy(img)
    for i in range(nova_img.shape[0]):
        for j in range(nova_img.shape[1]):
            if thresh[i, j]==255:
                nova_img[i,j,0]=np.clip(nova_img[i,j,0] + 50, 0, 255)
                nova_img[i,j,1]=np.clip(nova_img[i,j,1] + 50, 0, 255) 
                nova_img[i,j,2]=np.clip(nova_img[i,j,2] + 50, 0, 255) 

    return nova_img






#imageA = cv2.imread('Imatges/imatge1.PNG')
#imageB = cv2.imread('Imatges/platja2.PNG')
#imageA = imutils.resize(imageA, width=640)
#imageB = imutils.resize(imageB, width=400)

#imatge_gir=rotate_image(imageA, 90)
#cv2.imwrite("results/mi_imagen_girada.jpg", imatge_gir)


#a,b,L=recortar_imagen(imageA, 20)
#cv2.imwrite("results/mi_imagen_tras1.jpg", a)
#cv2.imwrite("results/mi_imagen_tras2.jpg", b)


# Agrega ruido gaussiano a la imagen.
#noisy_img =add_gaussian_noise(imageA, 0, 10)
#cv2.imwrite("results/mi_imagen_ruido_gaussian.jpg", noisy_img)





