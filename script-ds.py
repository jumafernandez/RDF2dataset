#!/usr/bin/env python3
# coding: utf-8

import csv
import urllib

from hdt import HDTDocument
import pandas as pd

from constants import SEP
from settings import (
    HDT_FILE, DATASET_FILE, OUTPUT_DATASET_FILE, STATS_FILE,
    PREDICATES_EXCLUDED, QUERY, RATIO)
from functions import get_sujeto_atr, get_predicado_atr, get_objeto_atr


# HDTDocument creation
document = HDTDocument(HDT_FILE)

# Se hace la consulta de los triples en funcion del sujeto/predicado/objeto
(triples, cardinality) = document.search_triples("", "", QUERY)

print("{}: {} objetos.".format(QUERY, cardinality))

#%% Procesamiento
# triple = s p o
lista_objetos = []
for triple in triples:
    s, p, o = triple
    sujeto_descripcion, sujeto_URI = get_sujeto_atr(s)
    lista_objetos.append(sujeto_URI[1:-1])

numero=0

with open(DATASET_FILE, 'w', newline='') as csv_ds, open(STATS_FILE, 'w', newline='') as csv_stats:
    ds_writer = csv.writer(csv_ds, delimiter=SEP, quotechar='"', quoting=csv.QUOTE_MINIMAL, doublequote=True)
    st_writer = csv.writer(csv_stats, delimiter=SEP, quotechar='"', quoting=csv.QUOTE_MINIMAL, doublequote=True)

    ds_writer.writerow(['sujeto', 'predicado', 'objeto'])
    st_writer.writerow(['objeto', 'atributos_finales', 'atributos_originales'])

    for sujeto_URI in lista_objetos:
        (atributos, cantidad) = document.search_triples(sujeto_URI, "", "")
        sujeto_descripcion, sujeto_URI = get_sujeto_atr(sujeto_URI)
        sujeto_descripcion = urllib.parse.unquote(sujeto_descripcion)[1:-1]

        cantidad_atributos=0
        print('{}: {}'.format(numero, sujeto_descripcion))
        numero+=1
        for atr in atributos:
            # Levanto los atributos/subgrafos
            atr_sujeto, atr_predicado, atr_objeto = atr
            nombre_objeto=sujeto_descripcion

            # Parseo cada subgrafo que contiene el objeto buscado para obetner los atributos
            predicado_descripcion, predicado_URI = get_predicado_atr(atr_predicado)
            objeto_descripcion, objeto_URI, objeto_valor, objeto_tipo, objeto_literal = get_objeto_atr(atr_objeto)

            # Luego buscamos si el predicado se encuentra en esa lista, si está no lo guardamos
            predicado_importante=True
            for termino in PREDICATES_EXCLUDED:
                if termino in predicado_descripcion:
                    predicado_importante=False

            if predicado_importante:
                if predicado_descripcion.find("Template:") != -1:
                    predicado_importante=False

            # Si es un predicado importante lo guardamos
            if predicado_importante:
                cantidad_atributos+=1
                if not(objeto_literal):
                    value = objeto_descripcion[1:-1]
                else:
                    value = objeto_valor

                # Quito comillas dobles.
                if value and value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

                ds_writer.writerow([sujeto_descripcion, predicado_descripcion, value])

        # Cambio la descripción del recurso por el nombre del objeto en caso
        # que exista ese atributo para ese sujeto
        st_writer.writerow([nombre_objeto, cantidad_atributos, cantidad])


#%% Se levanta el dataset del csv
df_rdf = pd.read_csv(DATASET_FILE, sep=SEP)

#%% Preparación para el pivoteo del dataframe

# Trabajo en pivotear el dataframe para que me quede con formato dataset
# Genero un numero de nivel para cada predicado -por los predicados repetidos-
df_rdf['nivel_atributo'] = df_rdf.groupby(['sujeto', 'predicado']).cumcount()
# Concateno al predicado el nivel así unifico el nombre del predicado para el objeto
df_rdf['atributo']=df_rdf['predicado']+"_"+df_rdf['nivel_atributo'].map(str)
# Elimino las columnas que sobran
df_rdf = df_rdf.drop(columns=["nivel_atributo", 'predicado'])
# Pivoteo el dataframe
dataset=df_rdf.pivot(index='sujeto', columns='atributo', values='objeto')

#%% Eliminación de filas y columnas con missings
###############################################

filas_minimas=int(len(dataset.index)*RATIO)
# Se borran las columnas
columnas_minimas=int(len(dataset.columns)*RATIO)
dataset=dataset.dropna(thresh=filas_minimas, axis=1)
# Se borran las filas
columnas_minimas=int(len(dataset.columns)*RATIO)
dataset=dataset.dropna(thresh=columnas_minimas, axis=0)

# Se guarda el dataset
dataset.to_csv(OUTPUT_DATASET_FILE, index = None, header=True, sep=SEP)
#%% Se muestran los resultados
objeto_descripcion, objeto_URI, objeto_valor, objeto_tipo, objeto_literal = get_objeto_atr(QUERY)
print("###### RESULTADOS #########")
print("Objeto consultado: ", objeto_descripcion)
print("Registros: ", len(dataset.index))
print("Atributos: ", len(dataset.columns))
print("Proporcion de missings: ", dataset.isnull().sum(axis=0).mean()/len(dataset.index)*100)
print("##### FIN RESULTADOS #####")
