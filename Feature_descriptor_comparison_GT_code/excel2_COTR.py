import estudi_descriptors
import pandas as pd
import os
import imageio

l_descriptor=['COTR']
environment=0 #0 pc; 1 colab
fm=0

def excel_COTR(opt_CORT, model_CORT):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('analisi.xlsx', engine='xlsxwriter')

    file_list = os.listdir('/content/drive/MyDrive/images')  # Llista amb els noms de les imatges
    n_trasnf=10
    n_files=9 #Longitud diccionari results

    for j in range(len(file_list)):

        nom_imatge='/content/drive/MyDrive/images/'+ file_list[j]
        imageA = imageio.imread(nom_imatge, pilmode='RGB')

        for i in range(1,n_trasnf+1):#6 transf
            # Calcular los valores y añadirlos al DataFrame
            results = estudi_descriptors.TrasnfArt(imageA, i, file_list[j],l_descriptor,fm, environment, opt_CORT, model_CORT)
            print(results)
            df=pd.DataFrame(results)
            df['frame']=nom_imatge[8:]
            trasformacions=['Rotació 2º','Rotació 35º','Translació','Soroll 60','Soroll 90','Blurring 33','Blurring 53','Canvi il·luminació','Pols','Especularitat']
            df['transformació']=trasformacions[i-1]
            df.rename(index={0:'n_kpA', 1:'n_kpB', 2:'n_matches', 3:'n_inliers', 4:'matching_hability', 5:'recall', 6:'precision', 7:'repetivitat', 8:'dist_projeccions', 9:'p_random_punts_H',  10:'esparcitatA', 11:'esparcitatB', 12:'temps'}, inplace=True)
            if i==1 and j==0:
                df.to_excel(writer, sheet_name='Sheet1')
            else:
                df.to_excel(writer, sheet_name='Sheet1', startrow=j*n_files*n_trasnf+i*n_files-n_files+1, header=False)


    writer.close()

