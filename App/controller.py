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

from DISClib.ADT.indexminpq import contains
from App.model import MST
import config as cf
import model
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.ADT.graph import edges, gr
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

    landingpoints = mp.keySet(analyzer['landingpoints'])
    capitals = mp.keySet(analyzer['countrypoints'])
    capital = False
    vertexa = None
    vertexb = None
    for key in lt.iterator(capitals):
        if origin in key:
            vertexa = key
        if destination in key:
            vertexb = key
    if vertexa is not None and vertexb is not None:
        capital = True
    if not capital:
        for key in lt.iterator(landingpoints):
            dataentry = mp.get(analyzer['landingpoints'], key)
            entry = me.getValue(dataentry)
            if not vertexa and origin in entry['data']['name']:
                key = lt.firstElement(entry['points'])
                vertexa = key
            if not vertexb and destination in entry['data']['name']:
                key = lt.firstElement(entry['points'])
                vertexb = key
    clusters = model.connectedComponents(analyzer)
    samecluster = model.sameCluster(analyzer, vertexa, vertexb)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return ((clusters, samecluster), (delta_time, delta_memory))

def requerimiento2(analyzer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    lstcables = model.servedCables(analyzer)
    result = lt.newList()
    for cable in lt.iterator(lstcables[0]):
        lt.addLast(result, model.selectResult(cable, 'cable'))


    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return ((result, lstcables[1]), (delta_time, delta_memory))

def requerimiento3(analyzer, origin, destination):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    
    countries = mp.keySet(analyzer['countrypoints'])
    for key in lt.iterator(countries):
        if origin == key.split(',')[0]:
            vertexa = key
        if destination == key.split(',')[0]:
            vertexb = key
    model.minimumCostPaths(analyzer, vertexa)
    minpath = model.minimumCostPath(analyzer, vertexb)
    model.createMap(analyzer, minpath)
    

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return (minpath, (delta_time, delta_memory))

def requerimiento4(analyzer):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
 
    model.MST(analyzer)
    MSTcost = model.costMST(analyzer)
    numvertexs= model.numVertexsMST(analyzer)
    maxbranch = model.longuestBranch(analyzer)
    model.createMap(analyzer, analyzer['MST']['mst'])
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return ((maxbranch, (MSTcost, numvertexs)), (delta_time, delta_memory))

def requerimiento5(analyzer, landingpoint):
    delta_time = -1.0
    delta_memory = -1.0
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()  

    landingpoints = mp.keySet(analyzer['landingpoints'])
    capitals = mp.keySet(analyzer['countrypoints'])
    capital = False
    for key in lt.iterator(capitals):
        if landingpoint in key:
            vertex = key
            capital = True
    if not capital:
        for key in lt.iterator(landingpoints):
            dataentry = mp.get(analyzer['landingpoints'], key)
            entry = me.getValue(dataentry)
            if landingpoint in entry['data']['name']:
                key = lt.firstElement(entry['points'])
                vertex = key
    edges = model.afectedCountries(analyzer, vertex)
    model.createMap(analyzer, edges[0])
    

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return (edges[1], (delta_time, delta_memory))


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