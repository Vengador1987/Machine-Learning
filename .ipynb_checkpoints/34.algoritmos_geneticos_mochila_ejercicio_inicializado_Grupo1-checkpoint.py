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

# In[1]:


import random
import numpy as np


# In[2]:


probabilidad_cruce = 0.9
probabilidad_mutacion = 0.1


# In[3]:


n_genes = 20
peso_max = 2500
n_poblacion = 20 

# nombres = [f"objeto_{i}" for i in range(n_genes)]
# print(nombres)


# In[4]:


pesos = [random.randint(100, 400) for i in range(n_genes)]
print(pesos)


# In[5]:


valores = [random.randint(500, 800) for i in range(n_genes)]
print(valores)


# In[6]:


def inicializar_poblacion(n_poblacion, n_genes, peso_max):
    poblacion = list()

    while len(poblacion) < n_poblacion:
        individuo = [random.randint(0, 1) for i in range(n_genes)]

        peso_individuo = np.dot(individuo, pesos)

        if peso_individuo <= peso_max:
            poblacion.append(individuo)
    return poblacion


# In[7]:


poblacion = inicializar_poblacion(n_poblacion, n_genes, peso_max)
poblacion


# In[8]:


for num, individuo in enumerate(poblacion):
 print(num, np.dot(individuo, valores), np.dot(individuo, pesos))


# In[9]:


# Selección por torneo
def elegir_padre(poblacion, n_candidatos):
    
    candidatos = random.sample(population = poblacion, k = n_candidatos)
    
    lista_valor = list()

    for num, individuo in enumerate(candidatos):
        lista_valor.append([num, np.dot(individuo, valores)])

    seleccion = sorted(lista_valor, key = lambda x : x[1])[-1] # lista: [posicion, valor]
    
    padre = candidatos[seleccion[0]] # individuo padre a partir de "posicion"
    
    return padre


# In[10]:


k = 5

padre1 = elegir_padre(poblacion, k)
padre2 = elegir_padre(poblacion, k)
print(padre1)
print(padre2)


# In[11]:


def cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max):

    hijo1 = list()
    hijo2 = list()
    
    # Cruzamiento binario uniforme
    if random.random() < probabilidad_cruce:

        # 1: padre1, 2: padre2

        for i in range(n_genes):
            padre = random.randint(1, 2)
            if padre == 1:
                hijo1.append(padre1[i])
                hijo2.append(padre2[i])
            else:
                hijo1.append(padre2[i])
                hijo2.append(padre1[i])
    
        # Si alguno supera el peso máximo, se repite el proceso
        if (np.dot(hijo1, pesos) > peso_max) or (np.dot(hijo2, pesos) > peso_max):
            hijo1, hijo2 = cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max)
    
    else:
        # Si la probabilidad de cruce impide generar hijos, se repite el proceso
        hijo1, hijo2 = cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max)
    
    return hijo1, hijo2


# In[12]:


hijo1, hijo2 = cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max)


# In[13]:


hijo1


# In[14]:


hijo2


# In[15]:


# Mutación binaria
def mutacion(probabilidad_mutacion, hijo1, hijo2, peso_max):

    hijo1_copia = hijo1.copy()
    hijo2_copia = hijo2.copy()

    if random.random() < probabilidad_mutacion:
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

        # Si alguno supera el peso máximo, se repite el proceso
        if (np.dot(hijo1_copia, pesos) > peso_max) or (np.dot(hijo2_copia, pesos) > peso_max):
            hijo1, hijo2 = mutacion(probabilidad_mutacion, hijo1, hijo2, peso_max)
        
    else:
        pass
    
    return hijo1_copia, hijo2_copia


# In[16]:


hijo1 #[1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]


# In[17]:


hijo2


# In[18]:


def reemplazo(poblacion, hijo1, hijo2):
    # Reemplazo estacional con reemplazo aleatorio

    reemplazados = random.sample(population = poblacion, k = 2)

    for reemplazado in reemplazados:
        poblacion.remove(reemplazado)

    poblacion.append(hijo1)
    poblacion.append(hijo2)
    
    return poblacion


# In[19]:


poblacion = reemplazo(poblacion, hijo1, hijo2)
poblacion


# In[20]:


def mejor_individuo(poblacion):
    
    lista_valor = list()

    for num, individuo in enumerate(poblacion):
        lista_valor.append([num, np.dot(individuo, valores)])

    seleccion = sorted(lista_valor, key = lambda x : x[1])[-1] # lista: [posicion, valor]

    mejor = poblacion[seleccion[0]]
    
    return mejor


# In[21]:


mejor_individuo(poblacion)


# In[22]:


np.dot(mejor_individuo(poblacion), valores), np.dot(mejor_individuo(poblacion), pesos)


# In[23]:


def algoritmo_genetico_mochila(n_poblacion, n_genes, probabilidad_cruce, probabilidad_mutacion, peso_max):
    
    lista_mejores_individuos = list()
    
    # Inicialización
    poblacion = inicializar_poblacion(n_poblacion, n_genes, peso_max)
    k = 5
    for generacion in range(50):
        # Selección de padres
        print(generacion)
       
        padre1 = elegir_padre(poblacion, k)
        padre2 = elegir_padre(poblacion, k)
        
        print("Padres seleccionados")

        # Cruce
        hijo1, hijo2 = cruce(padre1, padre2, probabilidad_cruce, n_genes, peso_max)
        print("Cruce reralizado")
        # Mutación
        hijo1, hijo2 = mutacion(probabilidad_mutacion, hijo1, hijo2, peso_max)
        print("Mutación hecha")

        # Reemplazo
        poblacion = reemplazo(poblacion, hijo1, hijo2)
        
        lista_mejores_individuos.append(mejor_individuo(poblacion))
        print("Remplazo realizado")
    
    return lista_mejores_individuos


# In[ ]:


mejor_individuo = algoritmo_genetico_mochila(n_poblacion, n_genes, probabilidad_cruce, probabilidad_mutacion, peso_max)


# In[ ]:


mejor_individuo


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




