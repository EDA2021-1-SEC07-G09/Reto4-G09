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
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initAnalyzer():
    
    return model.initAnalyzer()

def loadData(analyzer):
    songfile1 = cf.data_dir + 'PrepData/connections.csv'
    input_file1 = csv.DictReader(open(songfile1, encoding='utf-8-sig'))
    songfile2 = cf.data_dir + 'PrepData/countries.csv'
    input_file2 = csv.DictReader(open(songfile2, encoding='utf-8'))
    songfile3 = cf.data_dir + 'PrepData/landing_points.csv'
    input_file3 = csv.DictReader(open(songfile3, encoding='utf-8'))
    
    for value in input_file2:
        model.addCountry(analyzer, value)
    
    for value in input_file3:
        model.addLandingPoint(analyzer, value)
    
    for value in input_file1:
        model.addPointConnection(analyzer, value)

    model.addLandingPointConnections(analyzer)
    

# Funciones para la carga de datos

# Funciones de ordenamiento
def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)

# Funciones de consulta sobre el catálogo
def requerimiento1(analizer):
    return model.requerimiento1(analizer)

def requrimiento2(analizer):
    return model.requerimiento2(analizer)

def requrimiento3(analizer):
    return model.requerimiento3(analizer)

def requrimiento4(analizer):
    return model.requerimiento4(analizer)

def requrimiento5(analizer):
    return model.requerimiento5(analizer)
