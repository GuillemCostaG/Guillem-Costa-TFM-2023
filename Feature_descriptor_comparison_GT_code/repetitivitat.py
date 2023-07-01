import math
import random

def punto_dentro_del_circulo(punto1, punto2, radio):
    # Calcular la distancia entre los dos puntos
    distancia = math.sqrt((punto2[0] - punto1[0])**2 + (punto2[1] - punto1[1])**2)

    # Verificar si la distancia es menor o igual al radio del círculo
    if distancia <= radio:
        return True
    else:
        return False

def calcular_repetitivitat(kpA,kpB,treshold):
    #treshold=radi cercle al que considero que son el mateix punt
    #agafem 100 aleatoris perque sigui mes rapid
    kpA=kpA[:100]
    kpB=kpB[:100]
    n=0
    for punt_A in kpA:
        for punt_B in kpB:
            if punto_dentro_del_circulo(punt_A, punt_B, treshold):
                n=n+1

    if len(kpA)>len(kpB):
        n_kp=len(kpB)
    else:
        n_kp=len(kpA)

    repetivilitat=n/n_kp

    return repetivilitat

