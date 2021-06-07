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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from typing import Coroutine

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT.graph import adjacentEdges, gr, vertices
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dfs
from DISClib.DataStructures import edge as e
from math import sin,cos,sqrt,asin,pi
import folium
import random
import time
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initAnalyzer():
    analyzer = {
                    'connections': None,
                    'countries': None,
                    'landingpoints': None,
                    'countrypoints' : None
                    }

    analyzer['countries'] = mp.newMap(numelements=236,
                                     maptype='PROBING')
    analyzer['landingpoints'] = mp.newMap(numelements=2000,
                                     maptype='PROBING')

    analyzer['countrypoints'] = mp.newMap(numelements=236,
                                     maptype='PROBING')

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=5000,
                                              comparefunction=cmpVertex)
    return analyzer

# Funciones para agregar informacion al catalogo

def addCountry(analyzer, datacountry):

    map = analyzer['countries']
    country = datacountry['CountryName']
    existcountry = mp.contains(map, country)
    if  not existcountry:
        mp.put(map, country, datacountry)

def addLandingPoint(analyzer, datalandingpoint):

    map = analyzer['landingpoints']
    landingpoint = datalandingpoint['landing_point_id']
    existlandingpoint = mp.contains(map, landingpoint)
    if not existlandingpoint:
        entry = {'data': datalandingpoint,
                    'points' : lt.newList()}
        mp.put(map, landingpoint, entry)

def addCablePoint (analyzer, landingpoint, cablepoint):

    map = analyzer['landingpoints']
    dataentry = mp.get(map, landingpoint)
    entry = me.getValue(dataentry)['points']
    contains = lt.isPresent(entry, cablepoint)
    if contains == 0:
        lt.addLast(entry, cablepoint)

def addCountryPoint(analyzer, countrypoint):

    country = countrypoint.split(',')
    country = country[len(country)-1]
    contains = mp.contains(analyzer['countries'], country)
    capital = mp.get(analyzer['countries'], country)
    capital = me.getValue(capital)['CapitalName']
    country = country + ','+ capital
    map = analyzer['countrypoints']
    existcountry = mp.contains(map, country)
    if existcountry:
        dataentry = mp.get(map, country)
        entry = me.getValue(dataentry)
    else:
        entry = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction= cmpPoint)
        mp.put(map, country, entry)
    contains = lt.isPresent(entry, countrypoint)
    if contains == 0:
        lt.addLast(entry, countrypoint)
    
def addPointConnection(analyzer, connection):

    origin = formatVertex(analyzer, connection,'origin')
    destination = formatVertex(analyzer, connection,'destination')
    coordinate1 = getCoordinate(analyzer, connection['origin'])
    coordinate2 = getCoordinate(analyzer, connection['destination'])
    distance = getDistance(coordinate1, coordinate2)
    addStop(analyzer, origin)
    addStop(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    addCablePoint(analyzer, connection['origin'], origin)
    addCablePoint(analyzer, connection['destination'], destination)
    addCountryPoint(analyzer, origin)
    addCountryPoint(analyzer, destination)

    return analyzer

def addLandingPointConnections(analyzer):

    lstpoints = mp.keySet(analyzer['landingpoints'])
    for key in lt.iterator(lstpoints):
        dataentry = mp.get(analyzer['landingpoints'], key)
        lstcables = me.getValue(dataentry)['points']
        i = 1
        while i < lt.size(lstcables):
            origin = lt.getElement(lstcables, i)
            destination = lt.getElement(lstcables, (i+1))
            addConnection(analyzer, origin, destination, 0)
            i += 1
        if lt.size(lstcables) >= 2:
            origin = lt.lastElement(lstcables)
            destination = lt.firstElement(lstcables)
            addConnection(analyzer, origin, destination, 0)
        
def addCountryConnections(analyzer):

    lstcountry = mp.keySet(analyzer['countrypoints'])
    for key in lt.iterator(lstcountry):
        dataentry = mp.get(analyzer['countrypoints'], key)
        lstpoint = me.getValue(dataentry)
        addStop(analyzer, key)
        coordinate1 = getCoordinate(analyzer, key.split(',')[0])
        for value in lt.iterator(lstpoint):
            coordinate2 = getCoordinate(analyzer, value.split(',')[0])
            distance = getDistance(coordinate1, coordinate2)
            addConnection(analyzer, key, value, distance)
            addConnection(analyzer, value, key, distance)

def addConnection(analyzer, origin, destination, distance):

    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

def addStop(analyzer, stopid):

    if not gr.containsVertex(analyzer['connections'], stopid):
        gr.insertVertex(analyzer['connections'], stopid)

    return analyzer

# Funciones para creacion de datos

def formatVertex (analyzer, connection, element):

    name = None
    if element == 'origin':
        name = connection['origin']
    else:
        name = connection['destination']
    dataentry = mp.get(analyzer['landingpoints'], name)
    entry = me.getValue(dataentry)['data']['name']
    entry = entry.split(',')
    entry = entry[0]+','+entry[len(entry)-1].lstrip()
    name = str(name + ','+ connection['cable_name']+ ','+ entry)

    return name

def getCoordinate (analyzer, vertex):

    contains = mp.contains(analyzer['countries'], vertex)
    if contains:
        dataentry = mp.get(analyzer['countries'], vertex)
        entry = me.getValue(dataentry)
        coordinate = (float(entry['CapitalLatitude']), float(entry['CapitalLongitude']))
    else:
        dataentry = mp.get(analyzer['landingpoints'], vertex)
        entry = me.getValue(dataentry)['data']
        coordinate = (float(entry['latitude']), float(entry['longitude']))

    return (coordinate)

def getDistance(coordinate1, coordinate2):

    distance = 2*6371000*asin(sqrt(sin((pi/180)*(coordinate2[0]-coordinate1[0])/2)**2 + cos((pi/180)*coordinate1[0])*cos((pi/180)*coordinate2[0])*sin((pi/180)*(coordinate2[1]-coordinate1[1])/2)**2))
    distance = float("%.2f" % distance)

    return distance

def selectResult(value, element):

    if element == 'country':
        return str("Pais: " + value['CountryName']+ " - Poblacion: "+ value['Population']+ " - Numero de usuarios: "+ value['Internet users'])
    elif element == 'landingpoint':
        return str("Landing point id: "+ value['landing_point_id']+ " - Nombre: "+ value['name']+ " - Latitud: "+ value['latitude']+ " - Longitud: "+ value['longitude'])
    else:
        value = value.split(',')
        return str('Landing point nombre: '+ value[len(value)-2] + value[len(value)-1] + ' - Pais: '+  value[len(value)-1]+ ' - Id: '+ value[0])

# Funciones de consulta

def connectedComponents(analyzer):
  
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])

    return scc.connectedComponents(analyzer['components'])

def sameCluster(analyzer, origin, destination):

    return scc.stronglyConnected(analyzer['components'], origin, destination)

def minimumCostPaths(analyzer, origin):

    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], origin)

    return analyzer

def minimumCostPath(analyzer, destination):
    
    path = djk.pathTo(analyzer['paths'], destination)

    return path

def MST (analyzer):

    analyzer['MST'] = prim.PrimMST(analyzer['connections'])

    return analyzer

def costMST (analyzer):

    cost = prim.weightMST(analyzer['connections'], analyzer['MST'])

    return cost

def numVertexsMST(analyzer):

    edges = analyzer['MST']['mst']
    print(mp.size(edges))
    map = mp.newMap(numelements=2000,maptype='PROBING')
    for edge in lt.iterator(edges):
        vertexa = e.either(edge)
        vertexb = e.other(edge, vertexa)
        contains = mp.contains(map, vertexa)
        if not contains:
            mp.put(map, vertexb, 'Exist')
        contains = mp.contains(map, vertexb)
        if not contains:
            mp.put(map, vertexb, 'Exist')

    return lt.size(map)

def longuestBranch(analyzer):

    mapvertex = analyzer['MST']['edgeTo']
    vertexs = mp.keySet(mapvertex)
    map = mp.newMap(numelements=2000,maptype='PROBING')
    maxbranch = None
    maxvertexs = 0
    for vertex in lt.iterator(vertexs):
        edge = mp.get(mapvertex, vertex)
        edge = me.getValue(edge)
        entry = lt.newList('ARRAY_LIST')
        lt.addLast(entry, edge)
        vertex = e.either(edge)
        recreateBranch (mapvertex, entry, vertex)
        mp.put(map, vertex, entry)
    vertexs = mp.keySet(map)
    for vertex in lt.iterator(vertexs):
        entry = mp.get(map, vertex)
        value = me.getValue(entry)
        if lt.size(value) > maxvertexs:
            maxvertexs = lt.size(value)
            maxbranch = value

    return maxbranch

def recreateBranch (mapvertex, entry, vertex):

    exist = mp.contains(mapvertex, vertex)
    if exist:
        edge = mp.get(mapvertex, vertex)
        edge = me.getValue(edge)
        lt.addLast(entry, edge)
        vertex = e.either(edge)
        recreateBranch (mapvertex, entry, vertex)

def afectedCountries (analyzer, vertex):

    adjacentedges = gr.adjacentEdges(analyzer['connections'], vertex)
    map = mp.newMap(numelements=100,maptype='PROBING')
    i = 1
    while i <= lt.size(adjacentedges):
        edge = lt.getElement(adjacentedges, i)
        pais = edge['vertexB'].split(',')
        if len(pais) > 3:
            pais = pais[len(pais)-1]
        else:
            pais = pais[0]
        contains = mp.contains(map, pais)
        if contains:
            entry = mp.get(map, pais)
            entry = me.getValue(entry)
            if e.weight(edge) < entry[0]:
                mp.put(map, pais, (e.weight(edge), i))
                lt.deleteElement(adjacentedges, entry[1])
            else:
                lt.deleteElement(adjacentedges, i)
        else:
            mp.put(map, pais, (e.weight(edge), i))
            i += 1
    orderededges = mergeSortEdges(adjacentedges, lt.size(adjacentedges))[0]

    return orderededges

def numEdges (analyzer, vertex):
    
    outdegree = gr.outdegree(analyzer['connections'], vertex)
    indegree = gr.indegree(analyzer['connections'], vertex)
    numedges = outdegree + indegree

    return numedges

def servedCables(analyzer):

    lstvert = gr.vertices(analyzer['connections'])
    map = mp.newMap(numelements=2000,maptype='PROBING')
    maxvert = lt.newList()
    maxdeg = 0
    for vert in lt.iterator(lstvert):
        vertex = vert.split(',')
        contains = mp.contains(map, vertex[0])
        if not contains:
            mp.put(map, vertex[0], 'exist')
            degree = numEdges(analyzer, vert)
            landingpoint = mp.contains(analyzer['landingpoints'], vertex[0])
            if landingpoint:
                dataentry = mp.get(analyzer['landingpoints'], vertex[0])
                lstpoint = me.getValue(dataentry)['points']
                if lt.size(lstpoint) >= 2:
                    degree -= 2
                    for key in lt.iterator(lstpoint):
                        if key != vert:
                            degree += (numEdges(analyzer, key)-2)
        if degree > maxdeg:
            maxvert = lt.newList()
            lt.addLast(maxvert, vert)
            maxdeg = degree
        elif degree == maxdeg:
            lt.addLast(maxvert, vert)
    return (maxvert, maxdeg)

def createMap(analyzer, lstconnections):

    map = folium.Map(location=[12.240859, -18.118127], tiles='CartoDB Positron', zoom_start=3, orldCopyJump=True)
    map.add_child(folium.LatLngPopup())
    for edge in lt.iterator(lstconnections):
        origin = e.either(edge).split(',')
        destination = e.other(edge).split(',')
        coordinate1 = getCoordinate(analyzer, origin[0])
        coordinate2 = getCoordinate(analyzer, destination[0])
        route = (coordinate1, coordinate2) 
        folium.PolyLine(route,  color="#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])).add_to(map)
    map.save('mapa.html')



# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVertex(vertexa, keyvalue):

    vertexb = keyvalue['key']
    if (vertexa == vertexb):
        return 0
    else:
        return -1

def cmpPoint(value1, value2):

    value1 = value1.split(',')
    value2 = value2.split(',')
    if (value1[0] == value2[0]):
        return 0
    else:
        return -1

def cmpCables(stop, keyvaluestop):

    stopcode = keyvaluestop['key']
    if (stop in stopcode):
        return 0
    else:
        return -1

def cmpKm(edge1, edge2):
    return float(e.weight(edge1)) > float(e.weight(edge2))

# Funciones de ordenamiento

def mergeSortEdges(lstevent, size):
    sub_list = lt.subList(lstevent, 1, size)
    sub_list = sub_list.copy()
    start_time = time.process_time()
    mergeSortList = mer.sort(sub_list, cmpKm)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000

    return (mergeSortList, elapsed_time_mseg)