#Codi python per fer ORB, BRISK, KAZE, AKAZE, SIFT, SURF a dues imatges i fer match


import numpy as np
import imutils #Paquet molt important amb funcions necessàries de openCV
import cv2
import time

def stitch(imageA, imageB, Tdet, ratio=0.75, reprojThresh=4.0):
    #images = Llista amb les 2 imatges 
    #ratio = opcional entre 0.7 i 0.8
    #reprojThresh = màxim pixel “wiggle room” permes per el RANSAC algorithm
    #showMatches = True indica que els keyponts emparellats es visualitzen

    # unpack the images, then detect keypoints and extract local invariant descriptors (features, ex:SIFT) from them

    total_time = 0
    start = time.time()

    (kpsA, featuresA,trA) = detectAndDescribe(imageA,Tdet)
    (kpsB, featuresB,trB) = detectAndDescribe(imageB,Tdet)

    #print(featuresA)
    #print(featuresB)
    if featuresA is None or featuresB is None:
        d={}
        d['kpsA']=[]
        d['kpsB']=[]
        d['featuresA']=[]
        d['featuresB']=[]
        d['matches']=[] 
        d['H']=[]
        d['status']=[]
        return (d,1000*total_time)        

    # match features between the two images
    M = matchKeypoints(kpsA, kpsB, featuresA, featuresB,ratio, reprojThresh,Tdet)

    end = time.time()
    total_time = total_time + (end - start-trA-trB) #Li resto el temps del if

    #print(kpsB)
    #print(featuresB)
    #print('numero features = '+str(len(featuresA))+', '+str(len(featuresB)))
    if M is None:
        d={}
        d['kpsA']=[]
        d['kpsB']=[]
        d['featuresA']=[]
        d['featuresB']=[]
        d['matches']=[] 
        d['H']=[]
        d['status']=[]


        return (d,1000*total_time)
    
    matches=M[0]
    H=M[1]
    status=M[2]

    d={}
    d['kpsA']=kpsA
    d['kpsB']=kpsB
    d['featuresA']=featuresA
    d['featuresB']=featuresB
    d['matches']=matches  
    d['H']=H
    d['status']=status


    return (d,1000*total_time)


#Donada una imatge detecta els keypoints i extrau descriptors locals invariants.
#En aquest exemple s'utilitza DoG i SIFT
def detectAndDescribe(image,tdet):
    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # detect and extract features from the image

    total_time = 0
    start = time.time()

    if tdet=='ORB':
        end = time.time()
        temps_resta = total_time + (end - start)

        descriptor = cv2.ORB_create()
    
    elif tdet=='SIFT':
        end = time.time()
        temps_resta = total_time + (end - start)
        descriptor = cv2.xfeatures2d.SIFT_create() 
        
    elif tdet=='AKAZE':
        end = time.time()
        temps_resta = total_time + (end - start)
        descriptor = cv2.AKAZE_create()
        
    elif tdet=='KAZE':
        end = time.time()
        temps_resta = total_time + (end - start)
        descriptor = cv2.KAZE_create() 
        
    elif tdet=='BRISK':
        end = time.time()
        temps_resta = total_time + (end - start)
        descriptor = cv2.BRISK_create() 
    
    elif tdet=='SURF':
        end = time.time()
        temps_resta = total_time + (end - start)
        descriptor = cv2.xfeatures2d.SURF_create() 



    #Troba features (SIFT) i keypoints (DOG)
    (kps, features) = descriptor.detectAndCompute(image, None)
        
    # convert the keypoints from KeyPoint objects to NumPy arrays
    kps = np.float32([kp.pt for kp in kps])

    # return a tuple of keypoints and features
    return (kps, features,temps_resta)


# match features between the two images retorna:
#matches =Llista de keypoints emparellats 
#H = homography matrix (3x3), obtinguda del algoritme de RANSAC 
#status = Llista d'indexos per indicar quins keypoints emparellats han estat verificats 
# amb èxit espacialment utilitzant RANSAC. 

def matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh,Tdet):
    #reprojThresh = màxim pixel “wiggle room” permes per el RANSAC algorithm
        
    #matcher = cv2.DescriptorMatcher_create('BruteForce')

    #Caclcula les maches amb les fetures de les 2 imatges i k=2 perquè 
    # retorni 2 maches epr cada fetaures. Fem aixo perquè volem aplicar 
    # el test de David Lowie (utilitzant el ratio) per treure els falsos positius
    #rawMatches = matcher.knnMatch(featuresA, featuresB, 2)

    #Hi ha una millor forma de fer el match depenent del tipus de detector

    if Tdet in ['ORB','BRISK', 'AKAZE']:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        rawMatches = matcher.knnMatch(featuresA,featuresB, k=2)

    elif Tdet in ['SIFT','KAZE', 'SURF']:
        matcher = cv2.BFMatcher(cv2.NORM_L2)
        rawMatches = matcher.knnMatch(featuresA,featuresB, k=2)
    
    else:
        matcher = cv2.DescriptorMatcher_create('BruteForce')
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)

              
    # Mirem si són falsos positius (Lowe’s ratio test)   
    #Crea el vector on ficarà els maches que no són falsos positius
    matches = []
    # loop over the raw matches
    for m in rawMatches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            matches.append((m[0].trainIdx, m[0].queryIdx))
        
    # computing a homography requires at least 4 matches
    if len(matches) > 4:
        # construct the two sets of points
        ptsA = np.float32([kpsA[i] for (_, i) in matches])
        ptsB = np.float32([kpsB[i] for (i, _) in matches])
        
        # compute the homography between the two sets of points
        (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
        # return the matches along with the homograpy matrix
        # and status of each matched point

        #Ara mateix no estic aplicant RANSAC!!!!
        #Per aplicar RANASAC he de treure de matches aquells que la llista status te =0
        #La llista status e suna llista amb 1 si el  match es correcte i 0 si no.
        return (matches, H, status)
        
    # otherwise, no homograpy could be computed
    return None


