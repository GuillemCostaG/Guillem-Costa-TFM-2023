#Cal anaconda!!!
#conda activate dfm
#python dfm.py --input_pairs image_pairs.txt

#hE DESACTIVAT EL RANSAC en el fitcher DeepFeatureMatcher linea 80

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 19:09:25 2021

@author: ufukefe
"""

import os
import argparse
import yaml
import cv2
from DeepFeatureMatcher import DeepFeatureMatcher
from PIL import Image
import numpy as np
import time

def config():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(
            description='Algorithm wrapper for Image Matching Evaluation',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--input_pairs', type=str)

        args = parser.parse_args()  

    with open("config.yml", "r") as configfile:
        config = yaml.safe_load(configfile)['configuration']
       
  
    # Construct FM object
    fm = DeepFeatureMatcher(enable_two_stage = config['enable_two_stage'], model = config['model'], 
                        ratio_th = config['ratio_th'], bidirectional = config['bidirectional'], )
    
    return fm


def dfm(img_A, img_B, fm):
 
    total_time = 0
        
    start = time.time()
    H, H_init, points_A, points_B = fm.match(img_A, img_B)
    end = time.time()

    #H_init Sense RANSAC
        
    total_time = total_time + (end - start)
        
    keypoints0 = points_A.T
    keypoints1 = points_B.T
        
    mtchs = np.vstack([np.arange(0,keypoints0.shape[0])]*2).T

            
    #print(f'n \n \nAverage time is: {round(1000*total_time/total_pairs,0)} ms' )   

    d={}
    d['kpsA']=keypoints0
    d['kpsB']=keypoints1
    d['matches']=mtchs 

    return (d,1000*total_time)
























