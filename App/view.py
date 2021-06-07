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
import webbrowser
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import stack
from DISClib.DataStructures import edge as e
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

def initAnalyzer():
    analyzer = controller.initAnalyzer()
    return analyzer

def loadData(analizer):
    return controller.loadData(analizer)


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        analyzer = initAnalyzer()
        result = loadData(analyzer)
        print("Cargando información de los archivos ....")
        print("El total de landing points cargados es de: ", gr.numVertices(analyzer['connections']),
        "\nEl total de conexiones entre landing points es de: ", gr.numEdges(analyzer['connections']),
        "\nEl total de países cargados es de: ", mp.size(analyzer['countries']),
        "\n\n ++++++ 1° Landing point cargado ++++++"+ "\n"+ result[0][1],
        "\n\n ++++++ Ultimo Pais cargado ++++++"+ "\n"+ result[0][0])
        print(mp.size(analyzer['countrypoints']))
        print("\nTiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")

    elif int(inputs[0]) == 2:
        origin = input("Ingresa el landing point origen: ")
        destination = input("Ingresa el landing point destino: ")
        result = controller.requerimiento1(analyzer, origin, destination)
        print('El número de componentes conectados es: ', result[0][0])
        if result[0][1]:
            print('Los landing point '+ origin, ' y '+ destination + ' estan en el mismo cluster')
        else: 
            print('Los landing point '+ origin, ' y '+ destination +  ' no estan en el mismo cluster')
        print("\nTiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
    elif int(inputs[0]) == 3:
        result = controller.requerimiento2(analyzer)
        for value in lt.iterator(result[0][0]):
            print(value)
        print('El anterior landing point tiene un total de ', result[0][1], ' interconexiones con cables')
        print("\nTiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
    
    elif int(inputs[0]) == 4:

        origin = input('Ingrese el pais de origen: ')
        destination = input('Ingrese el pais de destino: ')
        result = controller.requerimiento3(analyzer, origin, destination)
        if result[0] is not None:
            distance = 0
            while (not stack.isEmpty(result[0])):
                edge = stack.pop(result[0])
                distance += e.weight(edge)
                print(edge)
            print('La distancia es de ', distance, ' Km')
        else:
            print('No es posible establecer una conexion')
        
        print("\nTiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
        vermap = input('Desea observar el camino grafica en el mapa universal.')
        if vermap == 'si':
            webbrowser.open('mapa.html')
    elif int(inputs[0]) == 5:
        result = controller.requerimiento4(analyzer)
        if result[0][0] is not None:
            distance = 0
            while (not lt.isEmpty(result[0][0])):
                edge = lt.removeLast(result[0][0])
                distance += e.weight(edge)
                print(edge)
        print('El numero de vertices asociados a la red de expansion minima es de: ', result[0][1][1])
        print('El costo del MST es de ', result[0][1][0], ' Km')
        print('El costo de la rama mas larga es de ', distance, ' Km')
        print("\nTiempo [ms]: ", f"{result[1][0]:.3f}", "  ||  ",  "Memoria [kB]: ", f"{result[1][1]:.3f}")
    elif int(inputs[0]) == 6:
        #webbrowser.open('mapa.html')
        #controller.requerimiento5(analyzer)

    else:
        sys.exit(0)
sys.exit(0)
