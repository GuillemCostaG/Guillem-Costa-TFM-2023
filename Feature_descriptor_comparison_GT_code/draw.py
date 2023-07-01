import cv2
import os
import numpy as np
import plot_esparcitat
import plot_lineas_match
import plot_H_punts
import plot_imatge_transformada
import imatge_negre_text

def marcar_puntos(imagen, lista_puntos, color=1):
    """
    Dada una imagen y una lista de puntos, marca los puntos indicados en rojo en la imagen.
    """
    # Crea una nueva imagen basada en la original
    imagen_modificada = imagen.copy()
    
    # Define el color rojo
    if color == 1:
        color_punto = (0, 0, 255)
    elif color == 2:
        color_punto = (0, 255, 0)
    elif color == 3:
        color_punto = (255, 0, 0)

    
    # Dibuja un círculo rojo de radio 3 en cada punto de la lista
    for punto in lista_puntos:
        x, y = punto
        cv2.circle(imagen_modificada, (int(x), int(y)), 2, color_punto, -1)
    
    return imagen_modificada


def guardar(imatge, detector, nom_imatge, transf, environment, tipus):

    transformaicions=['Rotacio 2','Rotacio 15','Rotacio 35',
                      'Translacio 25','Translacio 53','Translacio 75',
                      'Soroll 30','Soroll 60', 'Soroll 90',
                      'Blurring 33','Blurring 43','Blurring 53',
                      'Canvi illuminacio 25', 'Canvi illuminacio 50', 'Canvi illuminacio 75',
                      'Pols 100','Pols 200','Pols 300',
                      'Especularitat 200']
    
    #Miro a on estic executant el codi per saber on guardar
    if environment==0:#pc
        result_path="results"
    elif environment==1: #colab
        result_path="/content/drive/MyDrive/results"

    if not os.path.exists(result_path):
        os.mkdir(result_path)
    
    if tipus==0:
        nom_carpeta_tipus='Plot Inliners'
    elif tipus==1:
        nom_carpeta_tipus='Plot Esparcitat'
    elif tipus==2:
        nom_carpeta_tipus='Plot Matches'
    elif tipus==3:
        nom_carpeta_tipus='Plot H random points'
    elif tipus==4:
        nom_carpeta_tipus='Plot imatge transformada'

    path_carpeta0 = result_path+'/' + nom_carpeta_tipus
    path_carpeta1 = path_carpeta0+'/' + detector
    path_carpeta2 = path_carpeta1 + '/' + transformaicions[transf-1]
    path_imatge = path_carpeta2 + '/' + nom_imatge
    #path_imatge = path_carpeta1 + '/' + transformaicions[transf-1]+nom_imatge  

    if not os.path.exists(path_carpeta0):
        os.mkdir(path_carpeta0)   

    if not os.path.exists(path_carpeta1):
        os.mkdir(path_carpeta1)

    if not os.path.exists(path_carpeta2):
        os.mkdir(path_carpeta2)    


    # Guardar la imagen resultante en la carpeta path_carpeta
    cv2.imwrite(path_imatge, imatge) 

    #cv2.imshow('resultat', imatge)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
 


def marcar_juntar_gurdar(imatgeA, imatgeB, kpA, kpB, detector, nom_imatge, transf, environment):
    #Funció que pinta els peypoints en le simatges A i B, junta le simatges i le sguarda en una sola foto en la capeta de la seva transformació

    #Creem les noves images amb punts
    Imtage_A_punts=marcar_puntos(imatgeA, kpA)
    Imtage_B_punts=marcar_puntos(imatgeB, kpB)

    #Juntem les imatges en 1 nova imatge
    concatenated_img = cv2.vconcat([Imtage_A_punts, Imtage_B_punts])

    #guardem la imtge en la carpeta correponent a la seva transformació
    
    guardar(concatenated_img, detector, nom_imatge, transf, environment, 0)


def plotejar_esparcitat(imatgeA, imatgeB, kpA, kpB, detector, nom_imatge, transf, environment):

    plotA=plot_esparcitat.grafic_esparcitat(imatgeA,kpA, 0)

    plotB=plot_esparcitat.grafic_esparcitat(imatgeB,kpB, transf)

    concatenated_img = cv2.vconcat([plotA, plotB])
    
    #guardem la imtge en la carpeta correponent a la seva transformació
    
    guardar(concatenated_img, detector, nom_imatge, transf, environment, 1)


def plotejar_matches(imatgeA, imatgeB, inlinersA, inlinersB, detector, nom_imatge, transf, environment):

    Imatage_A_punts=marcar_puntos(imatgeA, inlinersA)
    Imatage_B_punts=marcar_puntos(imatgeB, inlinersB)

    nueva_imagen=plot_lineas_match.unir_matches(Imatage_A_punts, Imatage_B_punts, inlinersA, inlinersB)

    guardar(nueva_imagen, detector, nom_imatge, transf, environment, 2)


def plotejar_H_randorm_points(imagenA, imagenB, H_inliners,detector, nom_imatge, transf, environment):

    p_punts_distancia, mitja_d =plot_H_punts.plot_H_random_points(imagenA, imagenB, H_inliners, transf)

    #guardar(imatge_resultat, detector, nom_imatge, transf, environment, 3)

    return(p_punts_distancia, mitja_d)

def plotejar_imatge_transformada(imagenA, imagenB, H_inliners,detector, nom_imatge, transf, environment):

    out=plot_imatge_transformada.draw_imatge_transformada(imagenA, imagenB, H_inliners)

    guardar(out, detector, nom_imatge, transf, environment, 4)


def plot_imatge_negre(plot, detector, nom_imatge, transf, environment):

    imagen_negra = imatge_negre_text.crear_imagen_con_texto("No existeix H o val 0", 640, 480)

    if plot==3:
        guardar(imagen_negra, detector, nom_imatge, transf, environment, 3)

    if plot==4:
        guardar(imagen_negra, detector, nom_imatge, transf, environment, 4)
