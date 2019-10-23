# -*- coding: utf-8 -*-
import codecs
import sys
import argparse

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
                _temp += _list[x+y] # se lee y almacena el caracter acomulando en la variable _temp
            else:
                continue
        else:
            if(len(_temp) == n_grama):  # Cuando la longitud es la ideal, se agregan los caracteres a la lista
                msgList.append(_temp)

    msgList.sort() 
    return msgList


def SearchFrequency(msgList):
    matriz = []
    posList = 0
    for x in range(len(msgList)):
        count = 0
        # mientras los datos recorridos sean iguales, se aumenta la frecuencia de este
        while msgList[x] == msgList[posList]:
            count += 1  # es la variable que lleva la cantidad de veces que se repite un mismo caracter
            posList += 1
            if posList >= len(msgList):
                posList = 0
                
        else:
            if count > 0:  # Si se confirma que el contador es mayor que cero, existe 1 o mas veces el caracter
                # por lo tanto se agrega el caracter y su contador en una matriz
                matriz.append([msgList[x], count])
    return matriz  # por ultimo se devuelve la matriz con todos los datos y sus frecuencias


def OrganizeData(matriz, n_grama, dataDistance):

    text = '\nAnalisis Frecuencias Tamaño  n = ' + str(n_grama) + '\n'
    data = ''
    global frequency
    frequency += text
    matriz.sort(key=lambda x: x[1])
    MAX = matriz[len(matriz)-1][1]

    for x in range(0, len(matriz)):
        if (x % 5 == 0):  # en grupos de 5 se almacenan en una variable para despues llevar a un archivo
            frequency += '\n'
        frequency += ''+str(matriz[x][0])+':	'+str(matriz[x][1])+'		'

        por = round(matriz[x][1]*100/MAX)
        if(por >= 10):  # se buscan las frecuencias mas altas al 10% omitir los valores menos importantes
            if (x % 1 == 0):
                data += '\n '  
                data += '	'+str(matriz[x][0])+':	' + \
                    (var*por)+' 	'+str(matriz[x][1])
    frequency += '\n\n' + dataDistance + '\n'

    return (text + data)  

def SearchDistance(texto, msgList):
    posList = 0
    dataReport = ''
    for x in range(len(msgList)):
        position = 0
        stringPosition = ''
        stringChart = str(msgList[x]) + ': '
        stringDistance =  ''
        cont = 0
        
        while msgList[x] == msgList[posList]:
            if cont != 0:
                stringDistance += str(texto.find(msgList[x], position + 1) -  position ) + " -> "    
                position = texto.find(msgList[x], position + 1)
            else:
                position = texto.find(msgList[x], position)
                cont+=1
            stringPosition += str(position + 1) + ' '
            posList += 1
        
            if posList >= len(msgList):
                posList = 0
            if msgList[x] != msgList[posList]:
                dataReport += stringChart + stringPosition + '\nDistances: '  + stringDistance[:-4] + '\n\n'
                     
    return dataReport

if (len(sys.argv) == 5):
    if (args.file and args.num):
        textFile = open(str(args.file), 'r', encoding='utf-8')
        texto = textFile.read().upper().replace(' ', '')
        textFile.close()

        n_grama = int(args.num)

        for x in range(1, n_grama+1):
            msgList = ExtractList(texto, x)
            dataDistance = SearchDistance(texto, msgList)
            matriz = SearchFrequency(msgList)
            data = OrganizeData(matriz, x , dataDistance)
            graph += data

        file = open('reporte_frecuencias.txt', 'w' , encoding='utf-8', errors = 'ignore')
        file2 = open('grafico_frecuencias.txt', 'w', encoding='utf-8', errors = 'ignore')
        file.write(frequency + '\n')
        file2.write(graph + '\n')
        file.close()
        file2.close()
else:
    print('Uso: -f [archivo Lista] -n  [Numero de palabras]')
