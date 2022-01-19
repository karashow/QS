#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 14:31:13 2021

@author: eugenio
"""


from math import sqrt, ceil, floor, exp, log
from funzioni import next_prime, controllo, tonelli, modinv, gcd, nw_sqrt
from sistemi import riduci_matrice, trasponi, trova_soluzione

#
#   CRIVELLO QUADRATICO
#
      
##### BASE DI FATTORI
        
#Funzione che genera una base di fattori per N limitata da un bound B (numero di elementi della base di fattori)

def base_fattori(N,B):
    base_fattori = []
    k = 2
    i = 0
    while i < B-1:
        k = next_prime(k)
        if controllo(k, N):
            base_fattori.append(k)
            i += 1
    return base_fattori, i

##### TABELLE DA UTILIZZARE
    
#Funzione che ritorna tre vettori di numeri: 
#tabella_t                  contiene i numeri t(x) = (ceil(sqrt(N))+i)**2    
#tabella_valori             contiene i numeri y(x) = (ceil(sqrt(N))+i)**2-N
#tabella_valori_rip         è una copia di tabella_valori
    
def tabelle_dati(N,A):                                                              
    tabella_t = []
    tabella_valori = []
    tabella_valori_rip = []
    
    for i in range(A):
        tabella_t.append((ceil(sqrt(N))+i)**2)
        tabella_valori.append((ceil(sqrt(N))+i)**2-N)
        tabella_valori_rip.append((ceil(sqrt(N))+i)**2-N)
    
    return tabella_t, tabella_valori, tabella_valori_rip

#Funzione che ritorna una tabella con A righe e k colonne
    
def tabellone(A,k):
    tabellone=[]
    for i in range(A):
        riga=[]
        for j in range(k):
            riga.append(0)
        tabellone.append(riga)
    return tabellone

##### Una possibile implementazione del crivello quadratico: 


def crivello_quadratico(N, A, B):
    
    rad = ceil(sqrt(N))                  #Parte intera superiore di sqrt(N)
    
    [dato1, dato2, dato3] = tabelle_dati(N, A)        #Crea tre vettori di dati:
                                                 #dato1 contiene i valori di t(x)
                                                 #dato2 contiene i valori di y(x) e vengono man mano aggiornati
                                                 #dato3 contiene i valori di y(x) e non vengono modificati
    
    base, h = base_fattori(N, B)                     #base di fattori, h indica il numero di primi della base (senza contare il primo 2)
    
    tabella = tabellone(A, h + 1)                     #Crea la tabella le cui righe contengono le informazioni sugli esponenti dei numeri
                                                 # A righe x h+1 colonne
        
    if N % 2 == 1:                                 #Completa la prima colonna della tabella: cioè verifica le divisibilità per le potenze di 2
        if rad % 2 == 1:
            x = 0
        else:
            x = 1
    else:
        if rad % 2 == 1:
            x = 1
        else:
            x = 0
    while x < A:
        while dato2[x] % 2 == 0:
            tabella[x][0] += 1
            dato2[x] = dato2[x] // 2
        x = x + 2
    i = 1
    
    #Crivello Quadratico in cui si testano le divisibilità per le potenze di p al variare di p in base
    
    for primo in base:
        continua = True
        p = primo
        r = tonelli(N, primo)
        s = primo - r
        x = (r - rad) % primo
        y = (s - rad) % primo
        while continua:
            h = x
            k = y
            while h < A or k < A:
                if h < A:
                    tabella[h][i] += 1
                    dato2[h] = dato2[h] // primo
                    h = h + p
                if k < A:
                    tabella[k][i] += 1
                    dato2[k] = dato2[k] // primo
                    k = k + p
            
            p = p * primo
            x = (x - modinv(2 * (x + ceil(sqrt(N))), primo) * ((x + ceil(sqrt(N)))**2-N))%p
            y = (y-modinv(2*(y+ceil(sqrt(N))),primo)*((y+ceil(sqrt(N)))**2-N))%p
            
            if x >= A and y >= A:
                continua = False
                
        i = i+1
    #Dopo aver terminato il crivello si selezionano le righe del tabellone che corrispondono agli indici di dato2 che contengono 1
    
    v = []
    w = []
    matrix = []
    for indice in range(len(dato2)):
        if dato2[indice] == 1:
            v.append(floor(sqrt(dato1[indice])))
            w.append(dato3[indice])
            riga = []
            for j in range(len(base)+1):
                riga.append(tabella[indice][j])
            matrix.append(riga)
    
    base.insert(0,2)
            
    return base, v, w, matrix

#Funzione che, dato un numero intero N = p * q prodotto di due primi restituisce dei bound efficaci per il crivello quadratico 

def bound(N): 
    B = pow(exp(sqrt(log(N)*log(log(N)))), sqrt(2)/4)   #B indica la grandezza della base di fattori
    A = B**3                                            #A indica il numero di interi sui quali applicare il crivello
    return int(A),int(B)

            
def trova_quadrati(v, w, x):
    t = 1
    s = 1
    for i in range(len(x)):
        if x[i] == 1:
            t = t * v[i]
            s = s * w[i]
    s = nw_sqrt(s)      
    return t, s

#Funzione conclusiva, che trova un fattore di N composto.
#INPUT: N numero composto (per esempio prodotto di due primi)
#OUTPUT: un fattore di N oppure 'Bound troppo bassi, riprova'
    
def trova_fattore(N):
    A, B = bound(N)
    base, val_primo, val_secondo, tabella = crivello_quadratico(N, A, B)
    if val_primo == []:
        return 'Bound troppo bassi, riprova'
    
    u = riduci_matrice(tabella)
    u = trasponi(u)
    
    condizione = True
    
    while condizione:
        sol = trova_soluzione(u)
        t, s = trova_quadrati(val_primo, val_secondo, sol)
        x = gcd(t - s, N)
        if x != 1 and x != N:
            fattore = x
            condizione = False
    return fattore