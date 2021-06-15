#! /usr/bin/env python
# -*- coding: cp1251 -*-
"""Шаблон для созадния модулей
        для Python3"""

#-------------------------------------------------------------------------------
# Name:        Введите название модуля
#
# Author:
#
# Created:     15.02.2017
# Copyright:   (c) Кафедра геоинформатики и кадастра ННГАСУ 2017
#-------------------------------------------------------------------------------

#import os #Импорт модулей
import networkx as nx

def main():
    """
    Описание
    переменные
    результаты
    """
    FileName="Исходные дороги MIF/dor5.MIF"
    dicNodes,dicEdges=ReadMIF(FileName)
    #print(dicNodes)
    #print(dicEdges)
    G1= CreateGraph(dicNodes,dicEdges)
    #print(G1.nodes())

    #Выборка самого большого блока соединенных дорог
    #print('number_connected_components',nx.number_connected_components(G1))
    Gc = max(nx.connected_component_subgraphs(G1), key=len)
    #print(Gc.nodes())

    ExportGraphNodesToMIF(Gc,dicNodes,"Cохраненный файл графа дорог/graf.mif")

    #поиск кратчайшего пути
    FileName="Выгруженные маршруты в файле MIF и MID/5routes.mif"
    print("Маршрут 1")
    a=[]
    route=934,1476
    if nx.has_path(G1,route[0],route[1]):
        a=nx.shortest_path(G1,route[0],route[1],weight='weight')
        b=nx.shortest_path_length(G1,route[0],route[1],weight='weight')
        print('кратчaйший маршрут ',route[0],'-',route[1],':',a)
        print('длина маршрута:',b)
        ExportNodesToMIF1(a,b,dicNodes,FileName)
    else:
        print("путь не найден")

    print("Маршрут 2")
    a=[]
    route=934,912
    if nx.has_path(G1,route[0],route[1]):
        a=nx.shortest_path(G1,route[0],route[1],weight='weight')
        b=nx.shortest_path_length(G1,route[0],route[1],weight='weight')
        print('кратчaйший маршрут ',route[0],'-',route[1],':',a)
        print('длина маршрута:',b)
        ExportNodesToMIF2(a,b,dicNodes,FileName)
    else:
        print("путь не найден")

    print("Маршрут 3")
    a=[]
    route=934,1264
    if nx.has_path(G1,route[0],route[1]):
        a=nx.shortest_path(G1,route[0],route[1],weight='weight')
        b=nx.shortest_path_length(G1,route[0],route[1],weight='weight')
        print('кратчaйший маршрут ',route[0],'-',route[1],':',a)
        print('длина маршрута:',b)
        ExportNodesToMIF2(a,b,dicNodes,FileName)
    else:
        print("путь не найден")

    print("Маршрут 4")
    a=[]
    route=934,1307
    if nx.has_path(G1,route[0],route[1]):
        a=nx.shortest_path(G1,route[0],route[1],weight='weight')
        b=nx.shortest_path_length(G1,route[0],route[1],weight='weight')
        print('кратчaйший маршрут ',route[0],'-',route[1],':',a)
        print('длина маршрута:',b)
        ExportNodesToMIF2(a,b,dicNodes,FileName)
    else:
        print("путь не найден")

    print("Маршрут 5")
    a=[]
    route=934,115
    if nx.has_path(G1,route[0],route[1]):
        a=nx.shortest_path(G1,route[0],route[1],weight='weight')
        b=nx.shortest_path_length(G1,route[0],route[1],weight='weight')
        print('кратчaйший маршрут ',route[0],'-',route[1],':',a)
        print('длина маршрута:',b)
        ExportNodesToMIF2(a,b,dicNodes,FileName)
    else:
        print("путь не найден")


def ReadMIF(FileName):
    """
    Чтение файла MIF
    """
    f=open(FileName)
    Lines1=f.readlines()
    index1=0
    dicNodes={}
    dicEdges={}
    NodeCounter=0
    for Line1 in Lines1:

        if Line1[:5]=="Pline":
            #print (Line1)
            arrPlineCoord=ReadLine(Lines1,index1)
            #заполняю узлы
            for Pcoord1 in arrPlineCoord:
                key0=str(int(Pcoord1[0]))+"-"+str(int(Pcoord1[1]))
                if not key0 in dicNodes.keys():
                    NodeCounter+=1
                    dicNodes[key0]=[NodeCounter,Pcoord1[0],Pcoord1[1]]
            #заполняю словарь ребер
            for ind3 in range(len(arrPlineCoord)-1):
                keyPt1=str(int(arrPlineCoord[ind3][0]))+"-"+str(int(arrPlineCoord[ind3][1]))
                keyPt2=str(int(arrPlineCoord[ind3+1][0]))+"-"+str(int(arrPlineCoord[ind3+1][1]))
                Node1=dicNodes[keyPt1][0]
                Node2=dicNodes[keyPt2][0]
                keyEdge1=str(Node1)+"-"+str(Node2)
                dicEdges[keyEdge1]=[Node1,Node2,arrPlineCoord[ind3],arrPlineCoord[ind3+1]]
        #break
        index1+=1
    #Переделываю словарь узлов
    dicNodes2={}
    for key1 in dicNodes.keys():
        key2=dicNodes[key1][0]
        dicNodes2[key2]=dicNodes[key1][1:]
    return(dicNodes2,dicEdges)

def ReadLine(arrLines,PlineIndex):
    """
    Чтение координат полилинии
    """
    #print(arrLines[PlineIndex])
    Num1=int(arrLines[PlineIndex].split()[1])
    arrPlineCoord=[]
    for Line1 in arrLines[PlineIndex+1:PlineIndex+Num1+1]:
        arrCoord=Line1[:-1].split()
        x=float(arrCoord[0])
        y=float(arrCoord[1])
        arrPlineCoord.append([x,y])
        #print(x,y)
    return arrPlineCoord

def CreateGraph(dicNodes,dicEdges):
    """
    СОздание графа
    """
    G=nx.Graph()
    for key1 in dicEdges:
        x1=dicEdges[key1][2][0]
        y1=dicEdges[key1][2][1]
        x2=dicEdges[key1][3][0]
        y2=dicEdges[key1][3][1]
        dx=x2-x1
        dy=y2-y1
        S=(dx**2+dy**2)**(1/2)
        G.add_edge(dicEdges[key1][0],dicEdges[key1][1],weight=S)

    #вывод данных о графе
    #print('количество узлов:',G.number_of_nodes())
    #print('количество ребер:',G.number_of_edges())
    #nx.draw(G)
    #plt.show()
    return G

def ExportGraphNodesToMIF(G1,dicNodes,FileName):
    """
    Экспорт узлов в файл MIF
    """
    arrStr=[]
    arrStrMID=[]
    #Добавляем шапку файла
    arrStr.append("Version   300")
    arrStr.append('Charset "WindowsCyrillic"')
    arrStr.append('Delimiter ","')
    arrStr.append('CoordSys NonEarth Units "m" Bounds (-100000, -100000) (1000000, 1000000)')
    arrStr.append("Columns 1")
    arrStr.append("  num Char(10)")
    arrStr.append("Data")
    arrStr.append("")

    #Добавляем координаты из словаря узлов

    for node1 in G1.nodes():
        strData="Point "+str(dicNodes[node1][0])+" "+str(dicNodes[node1][1])
        arrStr.append(strData)
        arrStrMID.append(str(node1))

    #Запись в файл
    f = open( FileName, "w" )
    f.writelines( "%s\n" % item for item in arrStr )
    f.close()
    #запись файла MID
    f = open( FileName[:-3]+"mid", "w" )
    f.writelines( "%s\n" % item for item in arrStrMID )
    f.close()

def ExportNodesToMIF1(a,b,dicNodes,FileName):
    """
    Экспорт узлов в файл MIF
    """
    arrStr=[]
    arrStrMID=[]
    #Добавляем шапку файла
    arrStr.append("Version   300")
    arrStr.append('Charset "WindowsCyrillic"')
    arrStr.append('Delimiter ","')
    arrStr.append('CoordSys NonEarth Units "m" Bounds (-100000, -100000) (1000000, 1000000)')
    arrStr.append("Columns 3")
    arrStr.append("  NumberRoute Integer")
    arrStr.append("  route Char (12)")
    arrStr.append("  length_route Float")
    arrStr.append("Data")
    arrStr.append("")

    #Добавляем координаты из словаря узлов
    n=len(a)
    arrStr.append('Pline '+str(n))

    for a1 in a:
        for key1 in dicNodes.keys():
            if a1==key1:
                strData=str(dicNodes[key1][0])+" "+str(dicNodes[key1][1])
                arrStr.append(strData)


    #Запись в файл
    f = open( FileName, "w" )
    f.writelines( "%s\n" % item for item in arrStr )
    f.close()
    #запись файла MID
    arrStrMID.append('1,'+str(a[0])+'-'+str(a[n-1])+','+str(b))
    f = open( FileName[:-3]+"mid", "w" )
    f.writelines( "%s\n" % item for item in arrStrMID )
    f.close()

def ExportNodesToMIF2(a,b,dicNodes,FileName):
    #Добавляем координаты из словаря узлов
    arrStr=[]
    arrStrMID=[]
    n=len(a)
    arrStr.append('Pline '+str(n))

    for a1 in a:
        for key1 in dicNodes.keys():
            if a1==key1:
                strData=str(dicNodes[key1][0])+" "+str(dicNodes[key1][1])
                arrStr.append(strData)


    #Запись в файл
    f = open( FileName, "a" )
    f.writelines( "%s\n" % item for item in arrStr )
    f.close()
    #запись файла MID
    arrStrMID.append('1,'+str(a[0])+'-'+str(a[n-1])+','+str(b))
    f = open( FileName[:-3]+"mid", "a" )
    f.writelines( "%s\n" % item for item in arrStrMID )
    f.close()



#=========================================================================================================
if __name__ == '__main__':
    main()