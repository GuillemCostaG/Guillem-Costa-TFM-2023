
import imageio
import time
import numpy as np
from COTR.inference.sparse_engine import SparseEngine
import cv2

def matcher_COTR(img_a, img_b, opt, model):

    engine = SparseEngine(model, 32, mode='tile')
    t0 = time.time()
    corrs = engine.cotr_corr_multiscale_with_cycle_consistency(img_a, img_b, np.linspace(0.5, 0.0625, 4), 1, max_corrs=opt.max_corrs, queries_a=None)
    t1 = time.time()

    total_time=t1-t0

    #corrs es una llista de llistes amb el següent format: [[keypoint1 en A, keypoint1 en B], [keypoint2 en A, keypoint2 en B] , [keypoint3 en A, keypoint3 en B]]

    mkpts0=[]
    mkpts1=[]
    for m in corrs:
        mkpts0.append([m[0], m[1]])
        mkpts1.append([m[2], m[3]])



    #Creare la variable mtchs que sera una llista de llistas amb els matches amb el mateix format que la resta de descriptors
    #La llista serà [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10],..[len(mkpts0),len(mkpts0)]]
    mtchs =[[i, i] for i in range(0, len(mkpts0))] 
    #La llista serà


    (H, status) = cv2.findHomography(np.array(mkpts0),np.array( mkpts1), cv2.RANSAC, 4.0)

    d={}
    d['kpsA']=np.array(mkpts0)
    d['kpsB']=np.array(mkpts1)
    d['matches']=mtchs 
    d['H']=H
    d['status']=status

    return (d,1000*total_time)
    