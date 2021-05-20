"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar cantidad de clusteres (componentes conectados)")
    print("3- Landingpoint con mas interconexiones en la red")
    print("4- Ruta minima para enviar informacion entre dos paises")
    print("5- Identificar la red de expansion minima")
    print("6- Paises afectados por el fallo de un determinado landing point")

def initAnalizer():
    analizer = controller.initAnalizer()
    return analizer

def loadData(analizer):
    return controller.loadData(analizer)

analizer = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        initAnalizer()
        loadData(analizer)
        print("Cargando información de los archivos ....")

    elif int(inputs[0]) == 2:
        controller.requerimiento1(analizer)
    
    elif int(inputs[0]) == 3:
        controller.requerimiento2(analizer)
    
    elif int(inputs[0]) == 4:
        controller.requerimiento3(analizer)
    
    elif int(inputs[0]) == 5:
        controller.requerimiento4(analizer)
    
    elif int(inputs[0]) == 6:
        controller.requerimiento5(analizer)

    else:
        sys.exit(0)
sys.exit(0)
