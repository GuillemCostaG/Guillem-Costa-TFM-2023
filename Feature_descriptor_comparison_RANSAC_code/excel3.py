import estudi_descriptors
import cv2
import pandas as pd
import os

l_descriptor=['ORB','SIFT','BRISK','KAZE','AKAZE']
environment=0 #0 pc; 1 colab

if 'DFM' in l_descriptor:
    import dfm
    fm=dfm.config()
else:
    fm=0

if not os.path.exists('results'):
    os.mkdir('results')

if not os.path.exists('results/Excels'):
    os.mkdir('results/Excels')

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('results/Excels/analisi.xlsx', engine='xlsxwriter')

file_list = os.listdir('Dataset')  # Llista amb els noms de les imatges
file_list.sort()
transformaicions=['Rotacio 2','Rotacio 15','Rotacio 35',
                  'Translacio 25','Translacio 53','Translacio 75',
                  'Soroll 30','Soroll 60', 'Soroll 90',
                  'Blurring 33','Blurring 43','Blurring 53',
                  'Canvi_illuminacio 25', 'Canvi_illuminacio 50', 'Canvi_illuminacio 75',
                  'Pols 100','Pols 200','Pols 300',
                  'Especularitat 200']

d_results={0:'n_kpA', 1:'n_kpB', 2:'n_matches', 3:'n_inliers', 4:'matching_hability', 5:'recall', 6:'precision', 7:'repetivitat', 8:'dist_projeccions', 9:'p_random_punts_H',  10:'esparcitatA', 11:'esparcitatB', 12:'temps'}


n_trasnf=len(transformaicions)
n_files=len(d_results) #Longitud diccionari results

for j in range(len(file_list)):
    #Create a Pandas Excel writer using XlsxWriter as the engine per cada imatge
    writer_image = pd.ExcelWriter('results/Excels/analisi'+file_list[j]+'.xlsx', engine='xlsxwriter')

    nom_imatge='Dataset/'+ file_list[j]
    imageA = cv2.imread(nom_imatge)
    #imageA = cv2.imread('Dataset/First_Turbine_C_LE_5.png')
    #imageA = estudi_descriptors.resize_bordes(imageA)


    for i in range(1,n_trasnf+1):#6 transf
        # Calcular los valores y añadirlos al DataFrame

        results = estudi_descriptors.TrasnfArt(imageA, i, file_list[j],l_descriptor,fm, environment)
        print(results)
        df=pd.DataFrame(results)
        df['frame']=nom_imatge[8:]
        df['transformació']=transformaicions[i-1]
        df.rename(index=d_results, inplace=True)
        if i==1 and j==0:
            df.to_excel(writer, sheet_name='Sheet1')
            df.to_excel(writer_image, sheet_name='Sheet1')
        else:
            df.to_excel(writer, sheet_name='Sheet1', startrow=j*n_files*n_trasnf+i*n_files-n_files+1, header=False)
            df.to_excel(writer_image, sheet_name='Sheet1', startrow=i*n_files-n_files+1, header=False)
    writer_image.close()


writer.close()


