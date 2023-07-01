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
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    img1_torch = load_torch_image(img1).to(device)
    img2_torch = load_torch_image(img2).to(device)
    matcher = KF.LoFTR(pretrained='outdoor').to(device)


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
    (H, status) = cv2.findHomography(mkpts0, mkpts1, cv2.RANSAC, 4.0)
    
    mtchs =[[i, i] for i in range(0, len(mkpts0))] 
    d={}
    d['kpsA']=mkpts0
    d['kpsB']=mkpts1
    d['matches']=mtchs 
    d['H']=H
    d['status']=status

    return (d,1000*total_time)