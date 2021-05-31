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

    analyzer['countries'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['landingpoints'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['points'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=cmpId)
    return analyzer
# Funciones para agregar informacion al catalogo
def addCountry(analyzer, datacountry):
    map = analyzer['countries']
    country = datacountry['CountryName']
    existcountry = mp.contains(map, country)
    if existcountry:
        entry = mp.get(map, country)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, country, ltpista)
    lt.addLast(ltpista, datacountry)

def addLandingPoint(analyzer, datalandingpoint):

    landingpoint = datalandingpoint['landing_point_id']
    existlandingpoint = mp.contains(analyzer['landingpoints'], landingpoint)
    if existlandingpoint:
        dataentry = mp.get(analyzer['landingpoints'], landingpoint)
        entry = me.getValue(dataentry)
    else:
        entry = datalandingpoint
        mp.put(analyzer['landingpoints'], landingpoint, entry)

def addCablePoint (analyzer, landingpoint, cablepoint):
    existlandingpoint = mp.contains(analyzer['points'], landingpoint)
    if existlandingpoint:
        dataentry = mp.get(analyzer['points'], landingpoint)
        entry = me.getValue(dataentry)
    else:
        entry = lt.newList('ARRAY_LIST', cmpfunction = cmp)
        mp.put(analyzer['points'], landingpoint, entry)
    contains = lt.isPresent(entry, cablepoint)
    if contains == 0:
        lt.addLast(entry, cablepoint)

def addPointConnection(analyzer, connection):

    origin = formatVertex(analyzer, connection,'origin')
    destination = formatVertex(analyzer, connection,'destination')
    distance = getDistance(analyzer, connection['origin'], connection['destination'])
    addStop(analyzer, origin)
    addStop(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    addCablePoint(analyzer, connection['origin'], origin)
    addCablePoint(analyzer, connection['destination'], destination)

    return analyzer


def addStop(analyzer, stopid):

    if not gr.containsVertex(analyzer['connections'], stopid):
        gr.insertVertex(analyzer['connections'], stopid)

    return analyzer


def addRoutePoint(analyzer, service):

    entry = mp.get(analyzer['points'], service['cable_id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, service['cable_id'])
        mp.put(analyzer['points'], service['cable_name'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['cable_id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer    

def addLandingPointConnections(analyzer):

    lstpoints = mp.keySet(analyzer['points'])
    for key in lt.iterator(lstpoints):
        dataentry = mp.get(analyzer['points'], key)
        lstcables = me.getValue(dataentry)
        if lt.size(lstcables) >= 2:
            i = 1
            while i < lt.size(lstcables):
                origin = lt.getElement(lstcables, i)
                destination = lt.getElement(lstcables, (i+1))
                addConnection(analyzer, origin, destination, 0)
                i += 1
            origin = lt.lastElement(lstcables)
            destination = lt.firstElement(lstcables)
            addConnection(analyzer, origin, destination, 0)
        


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
    
def formatVertex (analyzer, connection, point):

    name = None
    if point == 'origin':
        name = connection['origin']
    else:
        name = connection['destination']
    dataentry = mp.get(analyzer['landingpoints'], name)
    entry = me.getValue(dataentry)['name']
    name = name + connection['cable_name'] + entry

    return name

# Funciones de consulta
def requerimiento1(analizer):
    return

def requerimiento1(analizer):
    return

def requerimiento1(analizer):
    return

def requerimiento1(analizer):
    return

def requerimiento1(analizer):
    return

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])

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
# Funciones de ordenamiento
