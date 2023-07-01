import matplotlib.pyplot as plt
import cv2
import kornia as K
import kornia.feature as KF
import numpy as np
import torch
import time

def load_torch_image(img):
    #Funico per pasar una imatge en format cv2.imread() a format de pytorch
    img = K.image_to_tensor(img, False).float() / 255.
    img = K.color.bgr_to_rgb(img)
    return img

def loftr_matcher(img1, img2):
    img1_torch = load_torch_image(img1)
    img2_torch = load_torch_image(img2)
    matcher = KF.LoFTR(pretrained='outdoor')

    total_time = 0 
    start = time.time()
    input_dict = {"image0": K.color.rgb_to_grayscale(img1_torch), # LofTR works on grayscale images only 
                "image1": K.color.rgb_to_grayscale(img2_torch)}

    with torch.inference_mode():
        correspondences = matcher(input_dict)

    end = time.time()      
    total_time = total_time + (end - start)

    mkpts0 = correspondences['keypoints0'].cpu().numpy()
    mkpts1 = correspondences['keypoints1'].cpu().numpy()
    Fm, inliers = cv2.findFundamentalMat(mkpts0, mkpts1, cv2.USAC_MAGSAC, 0.5, 0.999, 100000)
    inliers = inliers > 0
    
    #
    #correspondences['confidence'] hem diu la confianza (score) asignada a cada par de keypoints que se corresponden entre ambas imágenes. 
    #Fm es la matriu de rotació de RANSAC
    #inliers de monment no els utilitzo
    #mkpts0=Keypoints en la image A que han fet match amb la B
    #mkpts1=Keypoints en la image B que han fet match amb la A

    #Creare la variable mtchs que sera una llista de llistas amb els matches amb el mateix format que la resta de descriptors
    #La llista serà [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10],..[len(mkpts0),len(mkpts0)]]
    mtchs =[[i, i] for i in range(0, len(mkpts0))] 
    #La llista serà

    d={}
    d['kpsA']=mkpts0
    d['kpsB']=mkpts1
    d['matches']=mtchs 

    return (d,1000*total_time)


#rutaImatge1 = 'Imatges/platja1.PNG'
#rutaImatge2 = 'Imatges/platja2.PNG'
#img1 = cv2.imread(rutaImatge1)
#img2 = cv2.imread(rutaImatge2)

#(rmatch, t) = loftr_matcher(img1, img2)
#print(rmatch)
#print(t)
