#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:52:10 2019

@author: xiaoqiqi
"""
#import pandas as pd
#import numpy as np
#地源热泵系统图
#print('----------------------------------------')


#--------------------begin--------------------
#import
import json  
import numpy as np
import csv

#型号清单
f =open('models.json',encoding='utf-8')
models = json.loads(f.read())

#字典的json化
class element(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
class port(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
class line(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
        
#参考邻接矩阵
types=np.array(['地源热泵','水泵','末端'])
types_=np.array(['地源热泵_冷凝','地源热泵_蒸发','水泵','末端'])
connects=np.array([[0,1,-1],[-1,0,1],[1,-1,0]])
connects=np.array([[0,0,0,0],[0,0,-1,1],[0,1,0,-1],[0,-1,1,0]])
def typeIs(element):
    index = np.argwhere(types==element.type)
    return index[0][0]
def type_Is(port):
    index = np.argwhere(types==port.type)
    return index[0][0]

typess=np.array([''])
#连接函数
def connect(portA,portB):
    a = typeIs(portA)
    b = typeIs(portB)
    num = connects[a,b]
    return (num,a,b)

#--------------------模拟选型函数--------------------
def pump():
    return [element({
            
            }),element({
                    
                    }),element({
                            
                            })]
        
#--------------------读入设备列表--------------------
#读csv写入elements、ports、groups
elements=[]
ports=[]
mark_element=0
mark_port=0
with open('elements.csv')as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        port_=[]
        model = models[row[2]]
        #print(type(model))
        for each in model:
            for i in range(0,each['enter']):
                ports.append(port({
                        'name':row[0]+'_'+each['part']+'_enter_'+str(i+1),
                        'type':row[1]+'_'+each['part'],
                        'degree':each['enter_degree'],
                        'element':mark_element,
                        'line':[],
                        }))
                port_.append(mark_port)
                mark_port+=1
            for i in range(0,each['exit']):
                ports.append(port({
                        'name':row[0]+'_'+each['part']+'_exit_'+str(i+1),
                        'type':row[1]+'_'+each['part'],
                        'degree':each['exit_degree'],
                        'element':mark_element,
                        'line':[],
                        }))
                port_.append(mark_port)
                mark_port+=1
        elements.append(element({
                'name':row[0],
                'type':row[1],
                'model':row[2],
                'connection_':[],
                'port_':port_,
                }))
        mark_element+=1

print(elements)
print(ports)

#--------------------设备连接--------------------
connections=[]
mark_connection = 0
for i in range (0,len(elements)-1):
    for j in range(i+1,len(elements)):
        num,a,b = connect(elements[i],elements[j])
        if num!=0:
            connections.append(line({
                    'from':i if num>0 else j,
                    'to':j if num>0 else i,
                    'from_type':a if num>0 else b,
                    'to_type':b if num>0 else a,
                    'add':[],
                    }))
            elements[i].connection_.append(mark_connection)
            elements[j].connection_.append(mark_connection)
            mark_connection+=1

#print(elements)
#print(connections)
            
#--------------------设备布局--------------------
            
#未完成
            
#--------------------生成port列表--------------------
#lines

    
    