import cv2
import numpy as np
import imutils


#def get_pixel_rgb(event, x, y, flags, param):
    #if event == cv2.EVENT_LBUTTONDOWN:
        #pixel = nova_img[y, x]
        #print("Pixel RGB value at ({}, {}) : {}".format(x, y, pixel))

def augment_lum(intensitat):
    if intensitat in range(230,256):
        nova_intenistat=255
    elif intensitat in range(210,230):
        nova_intenistat=intensitat+25
    elif intensitat in range(190,210):
        nova_intenistat=intensitat+26
    elif intensitat in range(170,190):
        nova_intenistat=intensitat+20
    elif intensitat in range(160,170):
        nova_intenistat=intensitat+10
    elif intensitat<160:
        nova_intenistat=intensitat+5
    
    return nova_intenistat



# Cargar imagen
img = cv2.imread('Dataset/First_Turbine_A_MID_2.png')
img = imutils.resize(img, width=640)


def espec(img):
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización para crear máscara binaria
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

    nova_img = np.copy(img)
    for i in range(nova_img.shape[0]):
        for j in range(nova_img.shape[1]):
            if thresh[i, j]==255:
                nova_img[i,j,0]=np.clip(nova_img[i,j,0] + 50, 0, 255)
                nova_img[i,j,1]=np.clip(nova_img[i,j,1] + 50, 0, 255) 
                nova_img[i,j,2]=np.clip(nova_img[i,j,2] + 50, 0, 255) 
                #nova_img[i,j,0]=augment_lum(nova_img[i,j,0])
                #nova_img[i,j,1]=augment_lum(nova_img[i,j,1])
                #nova_img[i,j,2]=augment_lum(nova_img[i,j,2])
    

    
    return nova_img

nova_img=espec(img)
# Mostrar imagen original y máscara binaria
cv2.imshow('Imagen original', img)

cv2.imshow('Imatge nova', nova_img)
#cv2.setMouseCallback('Imatge nova', get_pixel_rgb)


cv2.waitKey(0)
cv2.destroyAllWindows()