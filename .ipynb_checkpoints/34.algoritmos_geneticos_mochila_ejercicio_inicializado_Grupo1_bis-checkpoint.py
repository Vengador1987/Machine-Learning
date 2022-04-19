#!/usr/bin/env python
# coding: utf-8

# ## Algoritmos Genéticos: Problema de la Mochila
# 
# Siguiendo los pasos de la teoria de Algoritmos Genéticos, has el algoritmo del problema de la mochila.
# 
# - Población Inicial: 20
# - Número de Genes: 20
# - Probabilidad de Cruce: 0.9
# - Probabilidad de Mutación: 0.1
# - Peso Maximo = 2500

import random
import numpy as np

probabilidad_cruce = 0.9
probabilidad_mutacion = 0.1


n_genes = 20
peso_max = 2500
n_poblacion = 20 

nombres = [f"objeto_{i}" for i in range(n_genes)]
# print(nombres)



pesos = [random.randint(100, 400) for i in range(n_genes)]
print(pesos)


valores = [random.randint(500, 800) for i in range(n_genes)]
print(valores)


def inicializar_poblacion(n_poblacion, n_genes, peso_max):
    poblacion = list()

    while len(poblacion) < n_poblacion:
        individuo = [random.randint(0, 1) for i in range(n_genes)]

        peso_individuo = np.dot(individuo, pesos)

        if peso_individuo <= peso_max:
            poblacion.append(individuo)
    return poblacion



poblacion = inicializar_poblacion(n_poblacion, n_genes, peso_max)
poblacion

for num, individuo in enumerate(poblacion):
    print(num, np.dot(individuo, valores), np.dot(individuo, pesos))


# Selección por torneo
def elegir_padre(poblacion, n_candidatos):
    
    candidatos = random.sample(population = poblacion, k = n_candidatos)
    
    lista_valor = list()

    for num, individuo in enumerate(candidatos):
        lista_valor.append([num, np.dot(individuo, valores)])

    seleccion = sorted(lista_valor, key = lambda x : x[1])[-1] # lista: [posicion, valor]
    
    padre = candidatos[seleccion[0]] # individuo padre a partir de "posicion"
    
    return padre

k = 5

padre1 = elegir_padre(poblacion, k)
padre2 = elegir_padre(poblacion, k)
print(padre1)
print(padre2)

def cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max, n_iteraciones = 0):
    
    # Cruzamiento binario uniforme
    if random.random() < probabilidad_cruce:

        peso_hijo1, peso_hijo2 = peso_max + 1, peso_max + 1

        while ((peso_hijo1 > peso_max) or (peso_hijo2 > peso_max)) and n_iteraciones < 100:
            hijo1, hijo2 = list(), list()
            for i in range(n_genes):
                padre = random.randint(1, 2)
                if padre == 1:
                    hijo1.append(padre1[i])
                    hijo2.append(padre2[i])
                else:
                    hijo1.append(padre2[i])
                    hijo2.append(padre1[i])
    
            peso_hijo1, peso_hijo2 = np.dot(hijo1, pesos), np.dot(hijo2, pesos)
            n_iteraciones += 1

        if (peso_hijo1 > peso_max) or (peso_hijo2 > peso_max):
            return padre1, padre2
        else:
            return hijo1, hijo2

    return padre1, padre2


hijo1, hijo2 = cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max)

hijo1
hijo2


# Mutación binaria
def mutacion(probabilidad_mutacion, hijo1, hijo2, peso_max, n_iteraciones = 0):

    if random.random() < probabilidad_mutacion:

        peso_hijo1, peso_hijo2 = peso_max + 1, peso_max + 1

        while ((peso_hijo1 > peso_max) or (peso_hijo2 > peso_max)) and (n_iteraciones < 100):

            hijo1_copia = hijo1.copy()
            hijo2_copia = hijo2.copy()

            posicion = random.randint(0, 19)
    #         print(posicion)

            if hijo1_copia[posicion] == 0:
                hijo1_copia[posicion] = 1
            else:
                hijo1_copia[posicion] = 0
            if hijo2_copia[posicion] == 0:
                hijo2_copia[posicion] = 1
            else:
                hijo2_copia[posicion] = 0

            peso_hijo1, peso_hijo2 = np.dot(hijo1_copia, pesos), np.dot(hijo2_copia, pesos)

            n_iteraciones += 1
        
        if (peso_hijo1 > peso_max) or (peso_hijo2 > peso_max):
            return hijo1, hijo2
        else:
            return hijo1_copia, hijo2_copia
    
    return hijo1, hijo2

hijo1 #[1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]
hijo2

def reemplazo(poblacion, hijo1, hijo2):
    # Reemplazo estacional con reemplazo aleatorio

    reemplazados = random.sample(population = poblacion, k = 2)

    for reemplazado in reemplazados:
        poblacion.remove(reemplazado)

    poblacion.append(hijo1)
    poblacion.append(hijo2)
    
    return poblacion

poblacion = reemplazo(poblacion, hijo1, hijo2)
poblacion

def mejor_individuo(poblacion):
    
    lista_valor = list()

    for num, individuo in enumerate(poblacion):
        lista_valor.append([num, np.dot(individuo, valores)])

    seleccion = sorted(lista_valor, key = lambda x : x[1])[-1] # lista: [posicion, valor]

    mejor = poblacion[seleccion[0]]
    
    return mejor

mejor_individuo(poblacion)

np.dot(mejor_individuo(poblacion), valores), np.dot(mejor_individuo(poblacion), pesos)


def algoritmo_genetico_mochila(n_poblacion, n_genes, probabilidad_cruce, probabilidad_mutacion, peso_max):
    
    lista_mejores_individuos = list()
    
    # Inicialización
    poblacion = inicializar_poblacion(n_poblacion, n_genes, peso_max)
    k = 5

    for generacion in range(1_00):

        # Selección de padres
        padre1 = elegir_padre(poblacion, k)
        padre2 = elegir_padre(poblacion, k)

        # Cruce
        hijo1, hijo2 = cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max)

        # Mutación
        hijo1, hijo2 = mutacion(probabilidad_mutacion, hijo1, hijo2, peso_max)

        # Reemplazo
        poblacion = reemplazo(poblacion, hijo1, hijo2)
        
        lista_mejores_individuos.append(mejor_individuo(poblacion))
    
    return lista_mejores_individuos


mejor_individuo = algoritmo_genetico_mochila(n_poblacion, n_genes, probabilidad_cruce, probabilidad_mutacion, peso_max)

import matplotlib.pyplot as plt

plt.plot(np.dot(mejor_individuo, valores), color = "red")
plt.plot(np.dot(mejor_individuo, pesos), color = "blue")
plt.ylim(0, 8000)
plt.show()

for i, j in zip(mejor_individuo[-1], nombres):
    if i == 1:
        print(i, j)