import numpy as np
import cv2
import imutils
import estudi_descriptors


def add_gaussian_noise(img, mean, std):
    noise = np.random.normal(loc=mean, scale=std, size=img.shape[:2])
    noisy_img = np.copy(img)
    for i in [0,1,2]:
        noisy_img[:,:,i] = np.clip(img[:,:,i] + noise, 0, 255).astype(np.uint8)
    return noisy_img

image = cv2.imread('Dataset/First_Turbine_A_MID_2.png')
image4=add_gaussian_noise(image, mean=0, std=60)
image4=estudi_descriptors.resize_bordes(image4)
image=estudi_descriptors.resize_bordes(image)



cv2.imshow('Imagen real', image)
cv2.imshow('Imagen resultante4', image4)




cv2.waitKey(0)
cv2.destroyAllWindows()
