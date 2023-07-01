import estudi_descriptors
import cv2


imageA = cv2.imread('Dataset/First_Turbine_A_MID_1.png')
#imageA = cv2.imread('Imatges/platja1.PNG')
#imageA=estudi_descriptors.resize_bordes(imageA)


for i in range(1,20):
    a=estudi_descriptors.TrasnfArt(imageA,i,'First_Turbine_A_MID_1.png')
    print(a)