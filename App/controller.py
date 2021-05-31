"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
import csv
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initAnalyzer():
    
    return model.initAnalyzer()

def loadData(analyzer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    songfile1 = cf.data_dir + 'PrepData/connections.csv'
    input_file1 = csv.DictReader(open(songfile1, encoding='utf-8-sig'))
    songfile2 = cf.data_dir + 'PrepData/countries.csv'
    input_file2 = csv.DictReader(open(songfile2, encoding='utf-8'))
    songfile3 = cf.data_dir + 'PrepData/landing_points.csv'
    input_file3 = csv.DictReader(open(songfile3, encoding='utf-8'))
    i = 1
    for value in input_file2:
        model.addCountry(analyzer, value)
        if i == 236:
            country = model.selectResult(value, 'country')
        i += 1
    i = 1
    for value in input_file3:
        model.addLandingPoint(analyzer, value)
        if i == 1:
            landingpoint = model.selectResult(value, 'landingpoint')
            i += 1
    
    for value in input_file1:
        model.addPointConnection(analyzer, value)

    model.addLandingPointConnections(analyzer)
    model.addCountryConnections(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return ((country, landingpoint), (delta_time, delta_memory))

    

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def requerimiento1(analyzer, origin, destination):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    cables = mp.keySet(analyzer['cables'])
    for key in lt.iterator(cables):
        if origin in key:
            vertexa = key
        if destination in key:
            vertexb = key
    clusters = model.connectedComponents(analyzer)
    samecluster = model.sameCluster(analyzer, vertexa, vertexb)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return ((clusters, samecluster), (delta_time, delta_memory))

def requrimiento2(analizer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    reprod = 0
    

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return model.requerimiento2(analizer)

def requrimiento3(analizer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    reprod = 0
    

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return model.requerimiento3(analizer)

def requrimiento4(analizer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    reprod = 0
    

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return model.requerimiento4(analizer)

def requrimiento5(analizer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    reprod = 0
    

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return model.requerimiento5(analizer)


def getTime():
        return float(time.perf_counter()*1000)

def getMemory():
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):

    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff

    delta_memory = delta_memory/1024.0
    return delta_memory