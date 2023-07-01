import descriptors
import imutils
import cv2
import numpy as np
import transformacions
import mesures
import draw
import repetitivitat


#Funió mach. Donades dues imatges i el tipus de detector retona
#Tipus de detector = 'ORB', 'SIFT', 'BRISK', 'KAZE', 'AKAZE', 'LOFTR', 'DFM','SURF'
def match(ImatgeA, ImatgeB, tdet, opt_CORT, model_COTR, fm, environment):

    if tdet in ['ORB', 'SIFT', 'BRISK', 'KAZE', 'AKAZE','SURF']:
        (rmatch, time) = descriptors.stitch(ImatgeA, ImatgeB, tdet) #diccionari amb 'kpsA' 'kpsB' 'featuresA' 'featuresB' 'matches' 
        #print(len(rmatch['matches']))
        #print(time)

        #KpsA = Llista de llistes on cada eleemnt de la llista es una coorednada de la imatge
        #featuresA = Lista de llistes on cada element es la feature corresponent a un kp (Per cada kpt em donen una feature)
        #matches = Llista de tuples on cada elemen és la posició de la llista KpA i KpB dels kpts que han fet match [(1,2),(3,5),(nºkpA,nºkpB)]
    
    #elif tdet == 'LOFTR':
        #rmatch = loftr.loftr_matcher(rutaImatge1, rutaImatge2)

    elif tdet =='DFM':
        import dfm
        (rmatch, time) = dfm.dfm(ImatgeA, ImatgeB,fm)#diccionari amb 'kpsA' 'kpsB' 'matches' 
        #print(len(rmatch['kpsA']),len(rmatch['matches']))
        #print(time)

        #KpsA = Llista de llistes on cada eleemnt de la llista es una coorednada de la imatge
        #matches = Llista de llistes on cada elemen és la posició de la llista KpA i KpB dels kpts que han fet match [(1,2),(3,5),(nºkpA,nºkpB)]

    elif tdet=='LOFTR':
        if environment==0:#pc
            import loftr
            (rmatch, time) = loftr.loftr_matcher(ImatgeA, ImatgeB)

        elif environment==1:#colab
            import loftr_cuda
            (rmatch, time) = loftr_cuda.loftr_matcher(ImatgeA, ImatgeB)           
            
        #KpsA=Keypoints en la image A que han fet match amb la B
        #KpsB=Keypoints en la image B que han fet match amb la A
    
    elif tdet=='COTR':
        import COTR_matcher
        (rmatch, time) = COTR_matcher.matcher_COTR(ImatgeA, ImatgeB, opt_CORT, model_COTR)


    return (rmatch, time)

def resize_bordes(img):
    #Funció que fa la imatge (480, 640, 3). Fica una bordes negres a la imatge adal i abaix  
    img=imutils.resize(img, width=640)
    new_img=img

    #Fica bordes negres a la imatge perque fagi 480 en la y.
    h, w, c = img.shape


    # calcular la cantidad de píxeles que se deben agregar en los lados
    border_width = int((480 - h) / 2)

    # crear una matriz de ceros del tamaño deseado
    new_img = np.zeros((480, w, c), dtype=np.uint8)

    # agregar los píxeles de la imagen original en el centro de la nueva matriz
    new_img[border_width:border_width+h, :, :] = img    
    
    return new_img

def resize_bodres_horitz(img):
    #Funcióq ue fica vores perquè la image tingui 640 d'ample
    h, w, c = img.shape

    
    # calcular la cantidad de píxeles que se deben agregar en los lados
    border_heigh = int((640 - w) / 2)

    # crear una matriz de ceros del tamaño deseado
    new_img = np.zeros((h, 640, c), dtype=np.uint8)

    # agregar los píxeles de la imagen original en el centro de la nueva matriz
    new_img[:, border_heigh:border_heigh+w, :] = img    
    
    return new_img

def array_list(array):
    #Funcio que donada una llista amb arrays dinre converteix la llista en un array de llistes
    l=[]
    for i in array:
        i_list=i.tolist()
        l.append(i_list)
    l=np.array(l)
    return l

def llista_matches(kpA,kpB,matches):
    #Funció que et dona 2 llistes:
    l_matches_A=[]#llista amb els punts que ha fet match de A
    l_matches_B=[]#llista amb els punts que ha fet match de B
    for match in matches:
        puntA=kpA[match[1]]
        l_matches_A.append(puntA)
        puntB=kpB[match[0]]
        l_matches_B.append(puntB)
    return (l_matches_A,l_matches_B)

def filtrar_coordenadas(coordenadas):
    #torna les posicions de la llista que estan fora de la imatge
    puntos_eliminados = []
    puntos_filtrados = []

    for i, punto in enumerate(coordenadas):
        x, y = punto
        if y < 60 or y > 420:
            puntos_eliminados.append(i)

    return puntos_eliminados

def filtar_matches(matches,puntos_eliminados_A,puntos_eliminados_B):
    matches_filtrat=[]
    for m in matches:
        posicio_A=m[1]
        posicio_B=m[0]
        if posicio_A not in puntos_eliminados_A or posicio_B not in puntos_eliminados_B:
            matches_filtrat.append(m)

    return matches_filtrat



def treure_punts_fora_imatge(rmatch):
    kypA = rmatch['kpsA']
    kypB = rmatch['kpsB']
    matches =rmatch['matches']

    puntos_eliminados_A=filtrar_coordenadas(kypA)
    puntos_eliminados_B=filtrar_coordenadas(kypB)

    matches_filtrat=filtar_matches(matches,puntos_eliminados_A,puntos_eliminados_B)

    rmatch['matches']=matches_filtrat

    return rmatch, len(puntos_eliminados_A), len(puntos_eliminados_B)
    



def TrasnfArt(imatgeA,transf, nom_imatge, descriptor, fm, environment, opt_CORT=0 ,model_COTR=0):

    #Fa la transformació
    M=0 #Assigna M=0 per els casos en que no són traslació no peti
    L=0
    #Rotació 2
    if transf == 1:
        imatgeA=resize_bordes(imatgeA)
        imatgeB, M=transformacions.rotate_image(imatgeA, 2)
        cv2.imwrite('iamtgeA.jpg', imatgeA) 
        cv2.imwrite('rotacio2.jpg', imatgeB) 
    
    #Rotació 15
    if transf == 2:
        imatgeA=resize_bordes(imatgeA)
        imatgeB, M=transformacions.rotate_image(imatgeA, 15)

    #Rotació 35º
    elif transf == 3:
        imatgeA=resize_bordes(imatgeA)
        imatgeB, M=transformacions.rotate_image(imatgeA, 35)
        #print(M)

    #Translació 25
    elif transf ==4:
        pixels=25
        percentatge_retallat=pixels*100/640
        imatgeA=resize_bordes(imatgeA)
        imatgeA, imatgeB, L = transformacions.recortar_imagen(imatgeA, percentatge_retallat)
        #Com hem retallat la imatge hem de ficar vores perquè sigui de 640 d'ample
        imatgeA=resize_bodres_horitz(imatgeA)
        imatgeB=resize_bodres_horitz(imatgeB)
 
    
    #Translació 53
    elif transf ==5:
        pixels=53
        percentatge_retallat=pixels*100/640
        imatgeA=resize_bordes(imatgeA)
        imatgeA, imatgeB, L = transformacions.recortar_imagen(imatgeA, percentatge_retallat)
        #Com hem retallat la imatge hem de ficar vores perquè sigui de 640 d'ample
        imatgeA=resize_bodres_horitz(imatgeA)
        imatgeB=resize_bodres_horitz(imatgeB)

    
    #Translació 75
    elif transf ==6:
        pixels=75
        percentatge_retallat=pixels*100/640
        imatgeA=resize_bordes(imatgeA)
        imatgeA, imatgeB, L = transformacions.recortar_imagen(imatgeA, percentatge_retallat)
        #Com hem retallat la imatge hem de ficar vores perquè sigui de 640 d'ample
        imatgeA=resize_bodres_horitz(imatgeA)
        imatgeB=resize_bodres_horitz(imatgeB)


    #Soroll 30
    elif transf ==7:
        imatgeB_GRAN = transformacions.add_gaussian_noise(imatgeA, mean=0, std=30)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Soroll 60
    elif transf ==8:
        imatgeB_GRAN = transformacions.add_gaussian_noise(imatgeA, mean=0, std=60)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Soroll 90
    elif transf ==9:
        imatgeB_GRAN = transformacions.add_gaussian_noise(imatgeA, mean=0, std=90)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Blurring 33
    elif transf == 10:
        imatgeB_GRAN = transformacions.blurring(imatgeA,33)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Blurring 43
    elif transf == 11:
        imatgeB_GRAN = transformacions.blurring(imatgeA,43)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Blurring 53
    elif transf == 12:
        imatgeB_GRAN = transformacions.blurring(imatgeA,53)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)

    
    #canvi iluminació 25
    elif transf == 13:
        imatgeB_GRAN = transformacions.canvi_ilum(imatgeA,25)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #canvi iluminació 50
    elif transf == 14:
        imatgeB_GRAN = transformacions.canvi_ilum(imatgeA,50)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #canvi iluminació 75
    elif transf == 15:
        imatgeB_GRAN = transformacions.canvi_ilum(imatgeA,75)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)



    #Pols 100
    elif transf ==16:
        imatgeB_GRAN=transformacions.pols(imatgeA,100)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Pols 200
    elif transf ==17:
        imatgeB_GRAN=transformacions.pols(imatgeA,200)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Pols 300
    elif transf ==18:
        imatgeB_GRAN=transformacions.pols(imatgeA,300)
        imatgeB=resize_bordes(imatgeB_GRAN)
        imatgeA=resize_bordes(imatgeA)


    #Especularitat 200
    elif transf ==19:
        imatgeA=resize_bordes(imatgeA)
        imatgeB=transformacions.especularitat(imatgeA,200)



    indicadors={}

 
    for detector in descriptor:#'LOFTR','COTR','SURF',['ORB','BRISK','SIFT','KAZE', 'AKAZE','DFM']['ORB','DFM']

        #Calculem els matches, kpts i temps
        (rmatch_no_filtrat, temps) = match(imatgeA, imatgeB, detector, opt_CORT, model_COTR,fm, environment)

        #Trec els kp i matches de forma de la imatge
        rmatch,n_kp_fora_A,n_kp_fora_B=treure_punts_fora_imatge(rmatch_no_filtrat)

        llista_kypA = rmatch['kpsA']
        llista_kypB = rmatch['kpsB']

        #INDICADORS QUE SI QUE VOLEN
        n_kpA = len(rmatch['kpsA'])-n_kp_fora_A
        n_kpB = len(rmatch['kpsB'])-n_kp_fora_B
        n_matches = len(rmatch['matches'])


        #INLINERS/OUTLINERS
        if n_matches!=0:
            #Calculem en numero d'inliners, el nº d'outliners, els punts en A que son inlienrs i els punts en B que són inliners 
            (inlinersA,inlinersB,dist_projeccions) = mesures.quality(llista_kypA, llista_kypB, rmatch['matches'], transf, M, L, 2)
            n_inliers=len(inlinersA)
            n_outliers=n_matches-n_inliers

            # % inliners
            precision=(n_inliers/n_matches)

            if n_kpA>n_kpB and n_kpB!=0:
                recall=(n_inliers/n_kpB)
            elif n_kpA<n_kpB and n_kpA!=0:
                recall=(n_inliers/n_kpA)
            else:
                recall=0
            

        else:
            #si no fa match
            (n_inliers,n_outliers,inlinersA,inlinersB)=(0,0,[],[])
            precision=0
            dist_projeccions=[0,0,0,0,0,0,0,0,0,0]
            recall=0
        

        (l_matches_A,l_matches_B)=llista_matches(llista_kypA, llista_kypB, rmatch['matches'])


        #Calcula la H amb els inliners       
        if len(inlinersA)>3:
            #Calulem la Holografic matrix
        
            inlinersA = array_list(inlinersA)
            inlinersB = array_list(inlinersB)

            H_inliner, _ = cv2.findHomography(inlinersA, inlinersB, cv2.RANSAC)
            
            if H_inliner is not None:
                #distancia que hi ha entre punts aleatoris calculats amb la H real i la H teorica
                H_existeix=True
            else:
                p_random_punts_H=[0,0,0,0,0,0,0,0,0,0]
                mitja_distancia_random_punts_H='inf'
                H_existeix=False
        else:
            H_inliner=[[0,0,0],[0,0,0],[0,0,0]]
            p_random_punts_H=[0,0,0,0,0,0,0,0,0,0]
            mitja_distancia_random_punts_H='inf'
            H_existeix=False
        
        #REPETIVILITAT I matching_hability
        if n_kpA>0 and n_kpB>0:
            repetivitat=repetitivitat.calcular_repetitivitat(llista_kypA,llista_kypB,0.0001)
            if n_kpA>n_kpB:
                matching_hability=n_matches/n_kpB
            else:
                matching_hability=n_matches/n_kpA
        else:
            repetivitat=0
            matching_hability=0
        

        #ESPARCITAT
        if len(inlinersA)>0:
            esparcitatA=mesures.esparcitat(imatgeA,np.array(inlinersA))
    
        else:
            esparcitatA='No hi han inliners'

        if  len(inlinersB)>0:
            esparcitatB=mesures.esparcitat(imatgeB,np.array(inlinersB))

        else:
             esparcitatB='No hi han inliners'

        #DIBUIX
        draw.marcar_juntar_gurdar(imatgeA, imatgeB, inlinersA, inlinersB, detector, nom_imatge, transf, environment)  
        
        draw.plotejar_esparcitat(imatgeA, imatgeB, inlinersA, inlinersB, detector, nom_imatge, transf, environment) 

        draw.plotejar_matches(imatgeA, imatgeB, inlinersA, inlinersB, detector, nom_imatge, transf, environment)


        if H_existeix==True:
            
            draw.plotejar_imatge_transformada(imatgeA, imatgeB, H_inliner,detector, nom_imatge, transf, environment)

            p_random_punts_H , mitja_distancia_random_punts_H=draw.plotejar_H_randorm_points(imatgeA, imatgeB, H_inliner,detector, nom_imatge, transf, environment)


        else:
            draw.plot_imatge_negre(3,detector, nom_imatge, transf, environment)#Si no existeix H en lloc de crear la el plot plotejar_imatge_transformada guardo una imatge en negre
            draw.plot_imatge_negre(4,detector, nom_imatge, transf, environment)#Si no existeix H en lloc de crear la el plot plotejar_H_randorm_points guardo una imatge en negre

    

        indicadors[detector]=[n_kpA, n_kpB, n_matches, n_inliers, matching_hability, recall, precision, repetivitat, dist_projeccions, p_random_punts_H,  esparcitatA, esparcitatB,temps]
        print(detector,transf, nom_imatge)
    
    return(indicadors)








