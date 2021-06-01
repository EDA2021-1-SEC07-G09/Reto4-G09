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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs
from math import sin,cos,sqrt,asin,pi
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
                    'points' : None
                    }

    analyzer['countries'] = mp.newMap(numelements=236,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['landingpoints'] = mp.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['points'] = mp.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['countrypoints'] = mp.newMap(numelements=236,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['cables'] = mp.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=cmpCables)

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=5000,
                                              comparefunction=cmpId)
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
        mp.put(map, landingpoint, datalandingpoint)

def addCablePoint (analyzer, landingpoint, cablepoint):

    map = analyzer['points']
    existlandingpoint = mp.contains(map, landingpoint)
    if existlandingpoint:
        dataentry = mp.get(map, landingpoint)
        entry = me.getValue(dataentry)
    else:
        entry = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction = cmp)
        mp.put(map, landingpoint, entry)
    contains = lt.isPresent(entry, cablepoint)
    if contains == 0:
        lt.addLast(entry, cablepoint)

def addCable (analyzer, cable):

    map = analyzer['cables']
    existcable = mp.contains(map, cable)
    if not existcable:
        mp.put(map, cable, 'exist')

def addCountryPoint(analyzer, countrypoint):

    country = countrypoint.split(',')
    country = country[len(country)-1].lstrip()
    map = analyzer['countrypoints']
    existcountry = mp.contains(map, country)
    if existcountry:
        dataentry = mp.get(map, country)
        entry = me.getValue(dataentry)
    else:
        entry = lt.newList(datastructure = 'ARRAY_LIST', cmpfunction = cmp)
        mp.put(map, country, entry)
    contains = lt.isPresent(entry, countrypoint)
    if contains == 0:
        lt.addLast(entry, countrypoint)
    
def addPointConnection(analyzer, connection):

    origin = formatVertex(analyzer, connection,'origin')
    destination = formatVertex(analyzer, connection,'destination')
    distance = getDistance(analyzer, connection['origin'], connection['destination'])
    addStop(analyzer, origin)
    addStop(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    addCablePoint(analyzer, connection['origin'], origin)
    addCablePoint(analyzer, connection['destination'], destination)
    addCountryPoint(analyzer, origin)
    addCountryPoint(analyzer, destination)
    addCable(analyzer, origin)

    return analyzer


def addStop(analyzer, stopid):

    if not gr.containsVertex(analyzer['connections'], stopid):
        gr.insertVertex(analyzer['connections'], stopid)

    return analyzer

def addLandingPointConnections(analyzer):

    lstpoints = mp.keySet(analyzer['points'])
    for key in lt.iterator(lstpoints):
        dataentry = mp.get(analyzer['points'], key)
        lstcables = me.getValue(dataentry)
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
        capital = mp.get(analyzer['countries'], key)
        capital = me.getValue(capital)['CapitalName']
        vertex = key + '-'+ capital
        addStop(analyzer, vertex)
        for value in lt.iterator(lstpoint):
            addConnection(analyzer, vertex, value, 0)
            addConnection(analyzer, value, vertex, 0)

def addConnection(analyzer, origin, destination, distance):

    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

# Funciones para creacion de datos

def getDistance (analyzer, origin, destination):

    dataentry1 = mp.get(analyzer['landingpoints'], origin)
    entry1 = me.getValue(dataentry1)
    dataentry2 = mp.get(analyzer['landingpoints'], destination)
    entry2 = me.getValue(dataentry2)
    coordinate1 = (float(entry1['latitude']), float(entry1['longitude']))
    coordinate2 = (float(entry2['latitude']), float(entry2['longitude']))
    distance = 2*6371000*asin(sqrt(sin((pi/180)*(coordinate2[0]-coordinate1[0])/2)**2 + cos((pi/180)*coordinate1[0])*cos((pi/180)*coordinate2[0])*sin((pi/180)*(coordinate2[1]-coordinate1[1])/2)**2))
    distance = float("%.2f" % distance)

    return distance
    
def formatVertex (analyzer, connection, element):

    name = None
    if element == 'origin':
        name = connection['origin']
    else:
        name = connection['destination']
    dataentry = mp.get(analyzer['landingpoints'], name)
    entry = me.getValue(dataentry)['name']
    name = str(name + ','+ connection['cable_name']+ ','+ entry)

    return name

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

def existPath (analyzer, origin, destination):

    analyzer['paths'] = dfs.DepthFirstSearch(analyzer['connections'], origin)
    exist = dfs.hasPathTo(analyzer['paths'], destination)

    return exist

def numEdges (analyzer, vertex, bool):
    
    outdegree = gr.outdegree(analyzer['connections'], vertex, bool)
    if bool:
        indegree = gr.indegree(analyzer['connections'], vertex)-(outdegree[0]-outdegree[1])
    else: 
        indegree = gr.indegree(analyzer['connections'], vertex)
    numedges = outdegree[1] + indegree

    return numedges

def servedCables(analyzer):

    lstvert = gr.vertices(analyzer['connections'])
    map = mp.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    maxvert = lt.newList()
    maxdeg = 0
    for vert in lt.iterator(lstvert):
        vertex = vert.split(',')
        contains = mp.contains(map, vertex[0])
        if not contains:
            mp.put(map, vertex[0], 'exist')
            degree = numEdges(analyzer, vert, True)
            exist = mp.contains(analyzer['points'], vertex[0])
            if exist:
                dataentry = mp.get(analyzer['points'], vertex[0])
                lstpoint = me.getValue(dataentry)
                i = 0
                for key in lt.iterator(lstpoint):
                    if i == 1:
                        degree += numEdges(analyzer, key, True)
                    else:
                        i += 1
            if degree > maxdeg:
                maxvert = lt.newList()
                lt.addLast(maxvert, vert)
                maxdeg = degree
            elif degree == maxdeg:
                lt.addLast(maxvert, vert)
    return (maxvert, maxdeg)



# Funciones utilizadas para comparar elementos dentro de una lista
def cmpId(stop, keyvaluestop):

    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def cmp(value1, value2):

    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return 1
    else:
        return -1

def cmpCables(stop, keyvaluestop):

    stopcode = keyvaluestop['key']
    if (stop in stopcode):
        return 0
    else:
        return -1
# Funciones de ordenamiento
