#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 18:49:07 2019

@author: juan
"""


#%% Funciones de parseo

def get_sujeto_atr(text):
    '''Se parsea el sujeto que siempre es como: http://dbpedia.org/resource/Lionel_Messi
        sujeto_descripcion=Lionel_Messi '''
    sujeto_descripcion = text.split("/")[len(text.split("/"))-1]
    # URI=http://dbpedia.org/resource/Lionel_Messi
    sujeto_URI = text
    sujeto_descripcion = '"' + sujeto_descripcion + '"'   
    sujeto_URI = '"' + sujeto_URI + '"'   

    return sujeto_descripcion, sujeto_URI

def get_predicado_atr(text):
    '''Se parsea el predicado, que siempre es: http://xmlns.com/foaf/0.1/surname
    predicado_descripcion=surname'''
    predicado_descripcion = text.split("/")[len(text.split("/"))-1]
    #predicado_URI=http://xmlns.com/foaf/0.1/surname
    predicado_URI = text

    return predicado_descripcion, predicado_URI

def get_objeto_atr(text):
    ''' Al objeto le hago un parseo especial, verifico si es un literal o no
        Si no es un literal, asumo que es un URI '''
    URI = '"' + text.replace('"', '""') + '"'
    # Solo para los objetos que son sujetos
    descripcion = None
    
    # Solo para los objetos que son literales
    valor = None
    tipo = None
  
    # Verifico si es un literal y actuo en consecuencia
    literal = not(text.find("http://")==0 and len(text)<=110)

    if (literal):
        numerico=text.find("^^")!=-1
        texto=text.find("@")!=-1
#        otro_tipo=not(texto or numerico)
        
        if numerico:
            valor = text.split("^^")[0].replace('"', "")
            tipo = '"' + text.split("^^")[1].replace("\n","") + '"' 
        elif texto:
            valor = '"' + text.split("@")[0].replace('"', "") + '"'
            tipo = '"' + text.split("@")[1].replace("\n","") + '"' 
#        elif (otro_tipo):
#            print(text)
    else: # Sino es literal, es URI 
        descripcion, URI = get_sujeto_atr(text)
    
    return descripcion, URI, valor, tipo, literal
