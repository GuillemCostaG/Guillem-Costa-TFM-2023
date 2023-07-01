import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.lines as mlines

# Ruta del archivo de Excel
#archivo_excel = 'results/Excels/analisiFirst_Turbine_A_MID_256.png.xlsx'
archivo_excel = 'analisi_10.06.2023_2.xlsx'

# Cargar el archivo de Excel en una variable de Pandas
datos_excel = pd.read_excel(archivo_excel)

# Cambiar el nombre de la primera columna
nuevo_nombre = 'Indicadors'
datos_excel = datos_excel.rename(columns={datos_excel.columns[0]: nuevo_nombre})

for e in ['temps','n_kpA','n_kpB','n_matches','n_inliers','matching_hability','recall','precision','repetivitat','esparcitatA','esparcitatB']:
    # Eliminar las filas con valor 'dist_projeccions' en la primera columna
    datos_excel = datos_excel.drop(datos_excel[datos_excel['Indicadors'] == e].index)

datos_excel = datos_excel.reset_index(drop=True)

llista_detectors=datos_excel.columns[1:-2]
numero_filas = datos_excel.shape[0]
diccionari_resultats={}

for fila in range(numero_filas-1):
    inidicador=datos_excel.loc[fila, 'Indicadors']
    transformacio=datos_excel.loc[fila, 'transformació']
    #print(datos_excel.loc[fila])
    nom_plot=str(inidicador)+'|'+str(transformacio)

    if nom_plot not in diccionari_resultats:
        #Creo el diccionari on guardare els valors si no existeix
        diccionari_valors_detector={}
    #Si ja existeix el diccionari
    else:
        diccionari_valors_detector=diccionari_resultats[nom_plot]

    for detector in llista_detectors:
        #Variable amb el valor del detcor
        valor_detector = datos_excel.loc[fila, detector]
        #Miro si existeix la llista dels valors de les imatges
        if detector not in diccionari_valors_detector:
            diccionari_valors_detector[detector] = []
        #Guardo els valors en el diccionari si no son strings
        if not isinstance(valor_detector, str):
            diccionari_valors_detector[detector].append(valor_detector)
        #converteixo les llistes en tipo llista abans era un str
        elif '[' in valor_detector:
            valor_detector = eval(valor_detector)
            diccionari_valors_detector[detector].append(valor_detector)
        else:
            #print('existeix un string'+' '+str(valor_detector))
            s=1

    diccionari_resultats[nom_plot]=diccionari_valors_detector


diccionari_resultats_filtrat={}
for clau in diccionari_resultats:
    #Trobar el nom dels garafics
    patron = r'(\w+\|\w+)'
    match = re.search(patron, clau)
    if match:
        nom_plot_filtrat = match.group(1)
    else:
        print("No se encontró el patrón en la cadena.")

    #Miro si existeix el diccionari
    if nom_plot_filtrat not in diccionari_resultats_filtrat:
        diccionari_resultats_filtrat[nom_plot_filtrat]={}
    
    diccionari_resultats_filtrat[nom_plot_filtrat][clau]=diccionari_resultats[clau]


claves_detect = ['ORB', 'SURF', 'SIFT', 'BRISK', 'KAZE', 'AKAZE', 'DFM', 'LOFTR', 'COTR']
colores = ['b', 'g', 'r', 'c', 'm', 'y', 'orange', 'purple', 'brown']
claves_detect_real=[]
colores_real=[]
nom_eix_y={'n_kpA':'Number of keypoints image A', 'n_kpB':'Number of keypoints image B', 'n_matches':'Number of matches', 'n_inliers':'Number of inliers', 'Matching Ability':'Matching Hability', 'recall':'Recall', 'precision':'Precision', 'repetivitat':'Repeatibility', 'dist_projeccions':'Percentage of inliers', 'p_random_punts_H':'Percentage of correct points',  'esparcitatA': 'Spread of inliers in image A', 'esparcitatB':'Spread of inliers in image B', 'temps':'Time[ms]'}
nom_eix_x={'Rotacio':'Rotated angle [degrees]','Translacio':'Translated pixels [pixels]','Soroll':'Noise','Blurring':'Blurring','Canvi_illuminacio':'Lighting change','Canvi':'Lighting change','Pols':'Number of dust particles','Especularitat':'Specularity'}
nom_title={'dist_projeccions':'Precision for different thresholds', 'p_random_punts_H':'Transformation distance'}

d_colors = dict(zip(claves_detect, colores))


# Recorrer el diccionario y las listas y calcular la media de los valores
for clave1, valor1 in diccionari_resultats_filtrat.items():
    # He de fer un gràfic per cada clau1
    diccionari_detectors = {}

    valors_eix_x = []

    for clave2, valor2 in valor1.items():
        print(str(clave2))


        for clave3, lista in valor2.items():


            llista_medias = []
            for valores in zip(*lista):
                media = sum(valores) / len(valores)
                llista_medias.append(media)

            if clave3 not in diccionari_detectors:
                diccionari_detectors[clave3] = []

            diccionari_detectors[clave3].append(llista_medias)

            if clave3 not in claves_detect_real:
                claves_detect_real.append(clave3)
                colores_real.append(d_colors[clave3])



        # Valores del eje x del gráfico
        numero = re.search(r'\d+$', str(clave2))
        numero = int(numero.group())
        valors_eix_x.append(numero)

    # Fer plot amb cada un dels diccionaris ex:

    partes = clave1.split('|')
    primer_string = partes[0]  # tempps, n_kpa, espacitat..
    segundo_string = partes[1]  # Pols, especularitat,cnvi ilu..

    detectors = lista_claves = list(diccionari_detectors.keys())

    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    fig = plt.figure(figsize=(11, 8))
    ax1 = fig.add_subplot(111)

    tipus_linea = ['-', '--', '-.']

    lines = []
    labels = []

    for detector in diccionari_detectors:
        t = 0
        for l_transfomacio in diccionari_detectors[detector]:
            y = np.array(l_transfomacio)

            c = d_colors[detector]
            line = ax1.plot(x, y, color=c, linestyle=tipus_linea[t])
            lines.append(line[0])
            labels.append(str(detector))
            t += 1

    plt.xticks(x)
    plt.xlabel('Pixels')
    plt.ylabel(nom_eix_y[primer_string])
    ax1.set_title(nom_title[primer_string])  # Añadir título al gráfico

    # Crear leyenda para el color del detector
    custom_lines_color = [mlines.Line2D([], [], color=c) for c in colores_real]
    lgn=ax1.legend(custom_lines_color, claves_detect_real, loc='upper center', bbox_to_anchor=(1.2, 1), title='Detector')
    ax1.add_artist(lgn)

    # Crear leyenda para los tipos de línea
    custom_lines_linestyle = [mlines.Line2D([], [], linestyle=ls) for ls in tipus_linea]
    ax1.legend(custom_lines_linestyle, valors_eix_x, loc='upper center', bbox_to_anchor=(1.2, 0.55), title=nom_eix_x[segundo_string])

    ax1.grid(True, linestyle='--')
    ax1.set_ylim(0, 1)
    ax1.set_xlim(1, 10)
    plt.subplots_adjust(right=0.75)

    plot_path='results/plots/'
    plot_intermitj=plot_path+'transformacions/'
    tranformacio_path=plot_intermitj+segundo_string
    indicador_path=tranformacio_path+'/'+primer_string

    if not os.path.exists(plot_path):
        os.mkdir(plot_path)
    
    if not os.path.exists(plot_intermitj):
        os.mkdir(plot_intermitj)

    if not os.path.exists(tranformacio_path):
        os.mkdir(tranformacio_path)

    path=indicador_path+'.png'

    plt.savefig(path)

    plot_intermitj=plot_path+'indicadors/'
    indicador_path=plot_intermitj+primer_string
    tranformacio_path=indicador_path+'/'+segundo_string
    

    if not os.path.exists(plot_path):
        os.mkdir(plot_path)

    if not os.path.exists(plot_intermitj):
        os.mkdir(plot_intermitj)

    if not os.path.exists(indicador_path):
        os.mkdir(indicador_path)

    path=tranformacio_path+'.png'

    plt.savefig(path)

    #plt.show()

