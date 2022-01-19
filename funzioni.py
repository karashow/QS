#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:54:21 2021

@author: eugenio
"""

from random import randint

#Calcolo della radice quadrata di un numero intero N utilizzando il metodo di Newton

def nw_sqrt(N):
    x = N
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + N // x) // 2
    return x


#Calcolo del massimo comun divisore: ritorna d = gcd(a, b)

def gcd(a, b):
    if a == 0:
        return b
    else:
        d = gcd(b % a, a)
        return d


#Algoritmo di Euclide esteso: ritorna la terna (d, x, y) tale che d = x*a + y*b

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
#Funzione che calcola l'inverso moltiplicativo, se esiste, di a modulo m

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    
#
#   RADICE QUADRATA MODULO p PRIMO
#
#
#
        
#Funzione che calcola il simbolo di Legendre (a/p) con p primo e a intero
    
def legendre(a, p):
    return pow(a, (p - 1) // 2, p)
        
#Controlla se N è un quadrato modulo p

def controllo(p,N):
    if legendre(N, p) == 1:
        return True
    else:
        return False

#Algoritmo di Tonelli-Shanks: dato n intero e p primo, n quadrato modulo p, restituisce una radice quadrata di n modulo p

def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r    


#
#   TEST DI PRIMALITA'
#
#
#    

#Questa funzione, dato n, ritorna la coppia (e, q) tali che n - 1 = (2 ** e) * q, q dispari

def parametri(n):
    e = 0
    q = n - 1
    while q % 2 == 0:
        e = e + 1
        q = q // 2
        
    return e, q    



#Test di primalità di Miller-Rabin: probabilità di errore <1/4.

def miller_rabin(n):
    k = 0
    x = randint(2, n - 1)
    d = gcd(x, n)
    if d > 1:
        return False
    else:
        e, q = parametri(n)
        if pow(x, q, n) == 1:
            return True
        else:
            while k < e:
                if pow(x, (2 ** k) * q, n) == n - 1:
                    return True
                else:
                    k = k + 1
            if k == e:
                return False
            
def is_prime(n):
    for i in range(5):
        if miller_rabin(n) == False:
            return False
    return True

def next_prime(n):
    continua = True
    while continua:
        if n % 2 == 0:
            n = n + 1
        else:
            n = n + 2
        if is_prime(n):
            continua = False
    return n
    