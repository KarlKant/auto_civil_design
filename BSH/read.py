#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:55:59 2019

@author: 谢秉辰
"""

import ifcopenshell
ifc_file = ifcopenshell.open("example.ifc")

#展示IFC文件中有哪些类型的节点
def print_type(ifc_file):
    products = ifc_file.by_type('IfcProduct')
    dock = []
    for product in products:
        flag = 0
        ship = product.is_a()
        for ship_ in dock:
            if ship == ship_:
                flag+=1
                break
        if flag == 0:
            dock.append(ship)
            print(ship)
        #product.ObjectPlacement.RelativePlacement.Location[0] 

#获取IFC文件中的所有Port        
def pick_sths(ifc_file,sth_str):
    sths = ifc_file.by_type(sth_str)
    return sths

#获取IFC文件中所有的连接关系
def pick_links(ifc_file):
    links = ifc_file.by_type('IFCRELCONNECTSPORTS')
    return links

#获取IFC文件中所有的 连接关系-PORT-ELEMENT
def pick_element(ifc_file):
    LPES=[]
    links = pick_links(ifc_file)
    for link in links:
        RelatingPort=link.RelatingPort
        RelatedPort=link.RelatedPort
        RelatingElement=link.RelatingPort.ContainedIn[0].RelatedElement
        RelatedElement=link.RelatedPort.ContainedIn[0].RelatedElement
        RelatingType=link.RelatingPort.ContainedIn[0].RelatedElement.is_a()
        RelatedType=link.RelatedPort.ContainedIn[0].RelatedElement.is_a()
        LPES.append([RelatingPort,RelatedPort,RelatingElement,RelatedElement,RelatingType,RelatedType])
    return LPES

#将不同类型的设备放置入不同的group，同时放入所有相关的连接信息。
    #主-客客客客……。主不可重复，客可以重复。
def pick_element_elements(ifc_file):
    count = 0
    LPES = pick_element(ifc_file)
    element_elements=[]
    lenx=len(LPES)
    for LPE in LPES:
        print(count,'/',lenx)
        count+=1
        element1 = LPE[2]
        element2 = LPE[3]
        flag = 0
        for element_element in element_elements:
            if element1 == element_element[0]:
                flag=0
                flag_=0
                for element in element_element[1]:
                    if element2 == element:
                        flag_=1
                        break
                if flag_==0:
                    element_element[1].append(element2)
                break
        if flag == 0:
            element_elements.append([element1,[element2,]])
        flag = 0
        for element_element in element_elements:
            if element2 == element_element[0]:
                flag=0
                flag_=0
                for element in element_element[1]:
                    if element1 == element:
                        flag_=1
                        break
                if flag_==0:
                    element_element[1].append(element1)
                break
        if flag == 0:
            element_elements.append([element2,[element1,]])
    return element_elements
    
    

#error:try definedBy    
def _definedby(ifc_file):
    xxx = pick_sths(ifc_file,'IfcFlowFitting')[0]
    for definition in xxx.IsDefinedBy:
        property_set = definition.RelatingPropertyDefinition
        print(property_set) # Might return Pset_WallCommon

#things about link
def _about_link():
    links = pick_links(ifc_file)
    print(links[0])#link
    print('============--------------============')
    print(links[0].RelatingPort)#link所连接的第一个port
    print(links[0].RelatedPort)#link所连接的第二个port
    print('============--------------============')
    print(links[0].RelatingPort.ContainedIn)#port所处的 port-element对应关系
    print('============--------------============')
    print(links[0].RelatingPort.ContainedIn[0].RelatedElement)#port对应的element
    
    
    print('============--------------============')
    for link in links:
        if len(links[0].RelatingPort.ContainedIn)!=1:
            print(len(links[0].RelatingPort.ContainedIn))
    print('============--------------============')
    
#types of elements
def type_of_elements(ifc_file):        
    LPES=pick_element(ifc_file)
    dock = []
    count = 0
    for LPE in LPES:
        ship = LPE[4]
        flag = 0
        for ship_ in dock:
            if ship == ship_:
                flag+=1
                break
        if flag == 0:
            dock.append(ship)
            print(ship)
        ship = LPE[5]
        flag = 0
        for ship_ in dock:
            if ship == ship_:
                flag+=1
                break
        if flag == 0:
            dock.append(ship)
            print(ship) 
        if LPE[4]=='IfcFlowController':
            print(LPE[2])
            count+=1
        if LPE[5]=='IfcFlowController':
            print(LPE[3])
            count+=1
    print(count)

#run run run ! ! !    
#run run run ! ! !   
#run run run ! ! ! 

x=pick_element_elements(ifc_file)
'''
element_elements = pick_element_elements(ifc_file)
for element_element in element_elements:
    print(element_element)
    '''













