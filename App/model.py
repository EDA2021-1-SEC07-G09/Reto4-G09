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
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initAnalizer():
    analyzer = {
                    'connections': None,
                    'countries': None,
                    'loandingpoints': None,
                    'points' : None
                    }

    analyzer['countries'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['loandingpoints'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)
    analyzer['points'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=cmpId)

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=cmpId)
# Funciones para agregar informacion al catalogo
def addCountry(analizer, datacountry):
    map = analizer['countries']
    country = datacountry['CountryName']
    existcountry = mp.contains(map, country)
    if existcountry:
        entry = mp.get(map, country)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, country, ltpista)
    lt.addLast(ltpista, datacountry)

def addLoandingpoint(analizer, datalandingpoint):
    map = analizer['landingponits']
    country = datalandingpoint['landing_point_id']
    existcountry = mp.contains(map, country)
    if existcountry:
        entry = mp.get(map, country)
        ltpista = me.getValue(entry)
    else:
        ltpista = lt.newList('ARRAY_LIST')
        mp.put(map, country, ltpista)
    lt.addLast(ltpista, datalandingpoint)

def addPointConnection(analyzer, lastservice, service):

    origin = formatVertex(lastservice)
    destination = formatVertex(service)
    cleanServiceDistance(lastservice, service)
    distance = float(service['cable_length'][:6]) - float(lastservice['cable_length'][:6])
    distance = abs(distance)
    addStop(analyzer, origin)
    addStop(analyzer, destination)
    addConnection(analyzer, origin, destination, distance)
    addRoutePoint(analyzer, service)
    addRoutePoint(analyzer, lastservice)
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


def addRouteConnections(analyzer):

    lststops = mp.keySet(analyzer['points'])
    for key in lt.iterator(lststops):
        lstroutes = me.get(analyzer['points'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route


def addConnection(analyzer, origin, destination, distance):

    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer
# Funciones para creacion de datos
def cleanServiceDistance(lastservice, service):

    if service['cable_length'] == '':
        service['cable_length'] = 0
    if lastservice['cable_length'] == '':
        lastservice['cable_length'] = 0


def formatVertex(service):

    name = service['cable_name'] + '-'
    name = name + service['cable_id']
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

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpId(stop, keyvaluestop):

    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):

    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
# Funciones de ordenamiento
