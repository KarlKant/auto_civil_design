#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:52:10 2019

@author: xiaoqiqi
"""
#import pandas as pd
#import numpy as np
#地源热泵系统图
elements=[]
element = {
        'name':'地源热泵A',
        'type':'地源热泵',
        'modal':'xxxxx1',
        'port':[],
        }
port = {
        'name':'地源热泵A节点1',
        'parent':'地源热泵A',
        }
element['port'].append(port)
port = {
        'name':'地源热泵A节点2',
        'parent':'地源热泵A',
        }
element['port'].append(port)
port = {
        'name':'地源热泵A节点3',
        'parent':'地源热泵A',
        }
element['port'].append(port)
port = {
        'name':'地源热泵A节点4',
        'parent':'地源热泵A',
        }
element['port'].append(port)
elements.append(element)
element = {
        'name':'水泵A',
        'type':'水泵',
        'modal':'yyyyy1',
        'port':[],
        }
port = {
        'name':'水泵A节点1',
        'parent':'水泵A',
        }
element['port'].append(port)
port = {
        'name':'水泵A节点2',
        'parent':'水泵A',
        }
element['port'].append(port)
elements.append(element)
element = {
        'name':'水泵B',
        'type':'水泵',
        'modal':'yyyyy1',
        'port':[],
        }
port = {
        'name':'水泵B节点1',
        'parent':'水泵B',
        }
element['port'].append(port)
port = {
        'name':'水泵B节点2',
        'parent':'水泵B',
        }
element['port'].append(port)
elements.append(element)
element = {
        'name':'末端O',
        'type':'末端',
        'modal':'zzzzz0',
        'port':[],
        }
port = {
        'name':'末端O节点1',
        'parent':'末端O',
        }
element['port'].append(port)
port = {
        'name':'末端O节点2',
        'parent':'末端O',
        }
element['port'].append(port)
elements.append(element)

connections = []
connections.append({
        'name':'连接1',
        'ports':['水泵B节点1','水泵B节点1','地源热泵A节点2'],
        'multiple':['水泵B节点1','水泵B节点1']
        })
connections.append({
        'name':'连接2',
        'ports':['水泵B节点2','水泵B节点2','末端O节点1'],
        'multiple':['水泵B节点2','水泵B节点2']
        })
connections.append({
        'name':'连接3',
        'ports':['末端O节点2','地源热泵A节点1'],
        'multiple':[]
        })

picture=['地源热泵A','连接1',['水泵1','水泵2'],'连接2','末端O','连接3','地源热泵A']

print(elements)
print(connections)