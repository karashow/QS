#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 11:18:11 2021

@author: eugenio
"""

from random import randint

#
#   RISOLUZIONE DI SISTEMI LINEARI A COEFFICIENTI IN GF(2)
#
#
#

#Funzione che restituisce il numero di righe e colonne di una matrice

def taglia(matrice):
    if matrice == []:
        return 0, 0
    else:
        righe = len(matrice)
        colonne = len(matrice[0])
    return righe, colonne

#Funzione che, data una matrice a coefficienti interi, restiruisce la sua riduzione modulo due

def riduci_matrice(matrice):
    a, b = taglia(matrice)
    for i in range(a):
        for j in range(b):
            matrice[i][j] = matrice[i][j] % 2    
    return matrice

#Funzione che data una matrice restituisce la sua trasposta
    
def trasponi(matrice):
    a, b = taglia(matrice)
    out = []
    for i in range(b):
        v = []
        for j in range(a):
            v.append(matrice[j][i])
        out.append(v)    
    return out

#Funzioni che implementano le operazioni elementari di riga
    
def scambia_righe(matrix, i, j):
    t = matrix[i]
    matrix[i] = matrix[j]
    matrix[j] = t
    return matrix

def somma_righe(matrix, i, j):
    l = len(matrix[i])
    for h in range(l):
        matrix[i][h] = (matrix[i][h] + matrix[j][h]) % 2    
    return matrix

#Eliminazione di Gauss
    
def eliminazione_di_gauss(matrix):
    a, b = taglia(matrix)
    continua = True
    i = 0
    pivot = i
    h = i
    while continua:
        #pivot = i
        trovato = False
        
        while trovato == False:
            if pivot < a:
                if matrix[pivot][i] == 1:
                    trovato = True
                else:
                    pivot = pivot + 1
            else:
                trovato = True
        if pivot < a:
            if pivot != h:
                scambia_righe(matrix, h, pivot)

            elimina = True
            j = h+1
            #k = i
            #if j < a:
            while elimina:
                if j >= a:
                    elimina = False
                else:
                    if matrix[j][i] == 1:
                        somma_righe(matrix, j, h)
                    j = j+1
            i = i+1
            h = h+1
            pivot = h
        else:
            pivot = h
            i = i+1 
        if i == b:
            continua = False
    return matrix

#Funzione che stabilisce se un vettore è nullo

def is_null(riga):
    for elemento in riga:
        if elemento != 0:
            return False
    return True

#Funzione che produce un vettore di zeri lungo n

def zero(n):
    z=[]
    for i in range(n):
        z.append(0)
    return z

#Funzione che produce un vettore lungo n che ha un uno in posizione indice e zero nelle altre

def vect(indice, n):
    vettore = zero(n)
    vettore[indice] = 1
    return vettore

#Funzione che restituisce la somma di due vettori

def somma(v, w):
    a = zero(len(v))
    for i in range(len(v)):
        a[i] = v[i] + w[i]
    return a
        
#Questa funzione prende un vettore di indici Y e un numero n. Restituisce tutti i possibili vettori lunghi n con degli uni al più nelle posizioni indicate in Y
#Quindi se Y contiene x elementi la funzione restituisce 2 ** x vettori lunghi n
    
def crea_sol(Y, n):
    sol = []
    if Y == []:
        sol.append(zero(n))
    else:
        index = Y[0]
        Y.pop(0)
        sol_prec = crea_sol(Y, n)
        for elem in sol_prec:
            sol.append(elem)
            sol.append(somma(elem, vect(index, n)))
    return sol

#Questa funzione prende un vettore di indici Y e un numero n. Restituisce un  possibile vettore lungo n con degli uni al più nelle posizioni indicate in Y

def crea_sol_bis(Y, n):
    sol = zero(n)
    if Y != []:
        for indice in Y:
            x = randint(0, 1)
            sol[indice] = x
    return sol
        
#Funzione che risolve il sistema Mx = 0 con M matrice a coefficienti in GF(2), cioè restistuisce TUTTE le soluzioni (MOLTO COSTOSO IN GENERALE)

def risolvi_sistema(matrix):
    
    a, b = taglia(matrix)
    g = eliminazione_di_gauss(matrix, a, b) 
    G = []
    for riga in g:
        if is_null(riga) == False:
            G.append(riga)

    c, d = taglia(G)
    pivot = zero(d)
    X =[]
    for i in range(c):
        trovato = False
        r = []
        for j in range(d):
            if trovato == False:
                if G[c-i-1][j] == 1:
                    pivot[j] = 1
                    x = j
                    trovato = True
            else:
                if G[c-i-1][j] == 1:
                    r.append(j)
        X.append([x, r])  
    Y = []
    for i in range(d):
        if pivot[i] == 0:
            Y.append(i)
            
    sol = crea_sol(Y, d)
    
    for vettore in sol:
       for elemento in X:
           a = elemento[0]
           b = elemento[1]
           
           if b != []:
               for pos in b:
                   vettore[a] = (vettore[a] + vettore[pos])%2
    return sol

def trova_soluzione(matrix):
    
    a, b = taglia(matrix)
    g = eliminazione_di_gauss(matrix) 
    G = []
    for riga in g:
        if is_null(riga) == False:
            G.append(riga)

    c, d = taglia(G)
    pivot = zero(d)
    X =[]
    for i in range(c):
        trovato = False
        r = []
        for j in range(d):
            if trovato == False:
                if G[c-i-1][j] == 1:
                    pivot[j] = 1
                    x = j
                    trovato = True
            else:
                if G[c-i-1][j] == 1:
                    r.append(j)
        X.append([x, r])  
    Y = []
    for i in range(d):
        if pivot[i] == 0:
            Y.append(i)
            
    sol = crea_sol_bis(Y, d)
    
    
    for elemento in X:
        a = elemento[0]
        b = elemento[1]
           
        if b != []:
            for pos in b:
                sol[a] = (sol[a] + sol[pos])%2
    return sol