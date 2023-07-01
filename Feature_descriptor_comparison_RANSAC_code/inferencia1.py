import estudi_descriptors
import cv2


img='First_Turbine_A_MID_1.png'
ubicacio='Dataset/'+img
imageA = cv2.imread(ubicacio)
#imageA = cv2.imread('Imatges/platja1.PNG')
#imageA=estudi_descriptors.resize_bordes(imageA)

l_descriptor=['DFM']
'''
'Rotacio 2'(1),'Rotacio 15'(2),'Rotacio 35'(3),
'Translacio 25(4)','Translacio 53'(5),'Translacio 75'(6),
'Soroll 30'(7),'Soroll 60'(8), 'Soroll 90'(9),
'Blurring 33'(10),'Blurring 43'(11),'Blurring 53'(12),
'Canvi illuminacio 25'(13), 'Canvi illuminacio 50'(14), 'Canvi illuminacio 75'(15),
'Pols 100'(16),'Pols 200'(17),'Pols 300'(18),
'Especularitat 200'(19)

'''
''''
for i in range(1,19):
    a=estudi_descriptors.TrasnfArt(imageA,i,'First_Turbine_A_MID_2.png',l_descriptor,0, 0)
    print(a)

'''
a=estudi_descriptors.TrasnfArt(imageA,8,img,l_descriptor,0, 0)
print(a)

