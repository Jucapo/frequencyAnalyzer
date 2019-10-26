# -*- coding: utf-8 -*-
import codecs
import sys
import argparse
import time

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Nombre de la lista")
parser.add_argument("-n", "--num", help="Numero de palabras")
args = parser.parse_args()


var = '▅' 
frequency = ''  
distance = ''
graph = ''  
totalwords = 0  
folder = []  
n_grama = 0  

key = [['A', 'B', 'C', 'D', 'E', 'F', 'G'],['H', 'I', 'J', 'K', 'L', 'M', 'N'],['Ñ', 'O', 'P', 'Q', 'R', 'S', 'T'],
['U', 'V', 'W', 'X', 'Y', 'Z', 'Ü'],['«', 'Ï', ']', 'À', '%', 'Ù', '\n'],['_', '[', '0', '1', '2', '3', '4'],
['5', '6', '7', '8', '9', '{', '}']]


def ExtractList(message, n_grama):
    msgList = []
    _list = list(message)
    _lLen = len(_list)

    for x in range(0, _lLen, n_grama):
        _temp = ''  # se almacena cada caracter hasta que se cumpla la longitud de n_grama
        for y in range(n_grama):
            if (x+y) < _lLen:               
                _temp += _list[x+y]
            else:
                continue
        else:
            if(len(_temp) == n_grama): 
                msgList.append(_temp)
    msgList.sort() 
    return msgList


def SearchFrequency(msgList):
    matriz = []
    posList = 0
    for x in range(len(msgList)):
        count = 0
        # se recorre la lista buscando los iguales y contando sus repeticiones
        while msgList[x] == msgList[posList]:
            count += 1  #numero de repeticiones
            posList += 1
            if posList >= len(msgList):
                posList = 0
        else:
            if count > 0: # mas de una repecion ? Si -> se agrega a la matriz
                matriz.append([msgList[x], count])
    return matriz  #  matriz con todas las cadenas y sus frecuencias


def OrganizeData(matriz, n_grama):

    text = '\nAnalisis Frecuencias Tamaño  n = ' + str(n_grama) + '\n'
    data = ''
    global frequency
    frequency += text
    matriz.sort(key=lambda x: x[1])
    MAX = matriz[len(matriz)-1][1]

    for x in range(0, len(matriz)):
        if (x % 5 == 0):  # se organizan las frecuencias en grupos de 5
            frequency += '\n'
        frequency += ''+str(matriz[x][0])+':	'+str(matriz[x][1])+'		'

        por = round(matriz[x][1]*100/MAX)
        if(por >= 10):  # se buscan las frecuencias que superen el rango del 10% 
            if (x % 1 == 0):
                data += '\n '  
                data += '	'+str(matriz[x][0])+':	' + \
                    (var*por)+' 	'+str(matriz[x][1])
    frequency += '\n\n'

    return (text + data)  

def SearchDistance(texto, msgList):
    posList = 0
    dataReport = ''
    for x in range(len(msgList)):
        position = 0
        stringPosition = ''
        stringChart = str(msgList[x]) + ': \nPositions: '
        stringDistance =  ''
        cont = 0
        
        while msgList[x] == msgList[posList]:
            if cont != 0:
                stringDistance += str(texto.find(msgList[x], position + 1) -  position ) + " -> "    
                position = texto.find(msgList[x], position + 1)
            else:
                position = texto.find(msgList[x], position)
                cont+=1
            stringPosition += str(position + 1) + '  '
            posList += 1
        
            if posList >= len(msgList):
                posList = 0
            if msgList[x] != msgList[posList]:
                file3.write(stringChart + stringPosition + '\nDistances:   '  + stringDistance[:-4] + '\n\n') 
    

if (len(sys.argv) == 5):
    if (args.file and args.num):
        textFile = open(str(args.file), 'r', encoding='ISO-8859-1')
        texto = textFile.read().upper().replace(' ', '')
        textFile.close()

        n_grama = int(args.num)
        file3 = open('reportes/reporte_distancias.txt', 'w')

        for x in range(1, n_grama+1):
            msgList = ExtractList(texto, x)
            SearchDistance(texto, msgList)
            matriz = SearchFrequency(msgList)
            data = OrganizeData(matriz, x)
            graph += data

        file = open('reportes/reporte_frecuencias.txt', 'w')
        file.write(frequency + '\n')
        file.close()

        with open('reportes/grafico_frecuencias.txt', "w", encoding="utf-8") as file2:
            file2.write(graph)
        file2.close()

        file3.close()
        print('\nTiempo de Ejecución:' + str(time.time()-start_time) + 'seg.\n')

else:
    print('\n\nUniversidad Autonoma de Occidente')
    print('  Juan Camilo Posso Ponce')
    print('  Jairo Torres\n\n')
    print('Referencias: Juan Carlos Trillos  (https://github.com/juanktrillos/Ply_Afp)\n\n')
    print('Uso: python3 frequencyAnalyzer.py -f Lista.txt -n  n-gramas \n\nEjemplo: python frequencyAnalyzer.py -f archivo.txt -n  3 \n\n')
