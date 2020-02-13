#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:50:35 2020

@author: xiaoqiqi
"""
#毕业论文中，数据结构对应字典，程序框图用来描述长函数




#--------------------begin--------------------
#import
import json
import numpy as np
import networkx as nx
import ezdxf

import matplotlib.pyplot as plt
count_outside_point=1
#plt.rcParams['font.family']=['Adobe Heiti Std'] #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


#读取system.json
f =open('system2.json',encoding='utf-8')
book = json.loads(f.read())
book_module = book["modules"]
book_rule = book["rules"]
book_rule_type = np.array(book_rule["module_types"])
book_rule_connects = book_rule["connects"]
system = book["system"]
#system["modules"],system["rules"]

#字典的json化
class module(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

class outside_port(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
        
class outside_line(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

#--------------------函数汇总--------------------
#typeIs函数
def moduleTypeIs(module):
    index = np.argwhere(book_rule_type==module["type"])
    return index[0][0]

#连接函数
def moduleConnect(moduleA,moduleB,i,j):
    a = moduleTypeIs(moduleA)
    b = moduleTypeIs(moduleB)
    num = book_rule_connects[a][b]
    if num!=0:
        ruleA = True
        ruleB = True
    else:
        ruleA = False
        ruleB = False
    for each_num in moduleA.rule:
        if system["rules"][each_num]["way"] == 'only' and ruleA and ruleB:
            if j in system["rules"][each_num]["group"]:
                return True
            else:
                return False
        if system["rules"][each_num]["way"] == 'exclusive' and ruleA and ruleB:
            if j in system["rules"][each_num]["group"] or\
            b not in system["rules"][each_num]["type"]:
                ruleA = True
            else:
                ruleA = False
        if system["rules"][each_num]["way"] == 'add':
           if j in system["rules"][each_num]["group"]:
                return True
    for each_num in moduleB.rule:
        if system["rules"][each_num]["way"] == 'only' and ruleA and ruleB:
            if i in system["rules"][each_num]["group"]:
                return True
            else:
                return False
        if system["rules"][each_num]["way"] == 'exclusive' and ruleA and ruleB:
            if i in system["rules"][each_num]["group"] or\
            a not in system["rules"][each_num]["type"]:
                ruleB = True
            else:
                ruleB = False
        if system["rules"][each_num]["way"] == 'add':
           if i in system["rules"][each_num]["group"]:
                return True
    return (ruleA and ruleB)
#excluesive表示一种同类排它性



#--------------------moudles生成与连接--------------------
#根据系统模块生成modules
modules=[]
repeat=[]
repeat_num=[]
position_xs=[]
position_ys=[]
for each in system["modules"]:
    typename = each["name"]
    flag = 0
    i=-1
    for i in range (0,len(repeat)):
        if repeat[i]==typename:
            flag=1
            repeat_num[i]+=1
            break
    if flag == 0:
        repeat.append(typename)
        repeat_num.append(1)
        i+=1
    position_x = book_module[each["name"]]['position_x']
    if position_x in position_xs:
        position_ys[position_xs.index(position_x)] += 5
        position_y = position_ys[position_xs.index(position_x)]
    else:
        position_xs.append(position_x)
        position_ys.append(0)
        position_y = 0
    modules.append(module({
            "name":typename+'_'+str(repeat_num[i]),#热泵水泵_01
            "typename":typename,#热泵水泵
            "rule":each["rule"],
            "type":book_module[each["name"]]['type'],#冷热源
            "elements":[],
            "inside_port_":[],
            "outside_port_":[],
            "position_x":position_x,
            "position_y":position_y,
            #"positions_x":[],
            #"positions_y":[],
            }))
       
#modules添加outside_port_，生成outside_ports
#同时记录rules
outside_ports_rules={}
outside_ports_degree={}
outside_ports=[]
count_outside_ports=0
for i in range(0,len(modules)):
    j=0
    for outside_port0 in book_module[modules[i].typename]['outside_ports']:
        j+=1
        outside_ports.append(outside_port({
                "name":modules[i].name+'_'+outside_port0['type']+'_'+str(j),
                "type":modules[i].type+'_'+outside_port0['type'],
                "degree":outside_port0['degree'],
                "father":i,#新生成的节点为-1
                "mother":(-1,-1),
                "line_":[],
                "position_x":modules[i].position_x+outside_port0['position_x'],
                "position_y":modules[i].position_y+outside_port0['position_y']
                }))
        outside_ports_rules[modules[i].type+'_'+outside_port0['type']]=\
        outside_port0["rules"]
        outside_ports_degree[modules[i].type+'_'+outside_port0['type']]=\
        outside_port0["degree"]
        modules[i].outside_port_.append(count_outside_ports)
        count_outside_ports+=1    
#print(outside_ports_rules)
    
    
#确定系统的连接,module_points
module_points=[]
module_lines=[]
for i in range(0,len(book_rule_connects)-1):
    for j in range(i+1,len(book_rule_connects)):
        print('--------------------------------------------------------')
        if book_rule_connects[i][j]==1:
            listA = []
            listB = []
            lista = []
            listb = []
            for k in range(0,len(modules)):
                typeK = moduleTypeIs(modules[k])
                if typeK == i:
                    listA.append([[k],[]]) 
                    lista.append(k)
                if typeK == j:
                    listB.append([[],[k]])
                    listb.append(k)
            for m in range(0,len(listA)):#lista[m]
                for n in range(0,len(listB)):
                    if moduleConnect(modules[lista[m]],modules[listb[n]],lista[m],listb[n]):
                        listA[m][1].append(listb[n])
                        listB[n][0].append(lista[m])
            listA_=[]
            listB_=[]
            for m in range(0,len(listA)):
                flag = -1
                for n in range(0,len(listA_)):
                    if listA[m][1]==listA_[n]["obj"]:
                        flag=n
                        break
                if flag == -1:
                    listA_.append({
                            "sub":listA[m][0],
                            "obj":listA[m][1]
                            })
                else:
                    listA_[flag]["sub"]=listA_[flag]["sub"]+listA[m][0]
            for m in range(0,len(listB)):
                flag = -1
                for n in range(0,len(listB_)):
                    if listB[m][0]==listB_[n]["obj"]:
                        flag=n
                        break
                if flag == -1:
                   listB_.append({
                            "sub":listB[m][1],
                            "obj":listB[m][0]
                            })
                else:
                    listB_[flag]["sub"]=listB_[flag]["sub"]+listB[m][1]
            points_=[]
            list_mark=[[],[]]
            for m in range(0,len(listA_)):
                for n in range(0,len(listB_)):
                    if (listA_[m]["sub"]==listB_[n]["obj"] or listA_[m]["obj"]==listB_[n]["sub"])\
                    and (set(listA_[m]["sub"]) <= set(listB_[n]["obj"]) and\
                         set(listB_[n]["sub"]) <= set(listA_[m]["obj"])):
                        points_.append({
                                "sub":listA_[m]["sub"]+listB_[n]["sub"],
                                "obj":list(set(listB_[n]["obj"])-set(listA_[m]["sub"]))+\
                                list(set(listA_[m]["obj"])-set(listB_[n]["sub"])),
                                "outside_port_":[],
                                "ports":[],
                                "lines":[]
                                })
                        list_mark[0].append(m)
                        list_mark[1].append(n)
            for m in range(0,(len(listA_))):
                if m not in list_mark[0]:
                    points_.append(listA_[m])
            for n in range(0,len(listB_)):
                if n not in list_mark[1]:
                    points_.append(listB_[n])
            lines_ = []
            for a in range(0,len(points_)-1):
                for b in range(i+1,len(points_)):
                    if set([])<set(points_[a]["obj"])<=set(points_[b]["sub"]) and\
                     set([])<set(points_[a]["obj"])<=set(points_[b]["sub"]):
                        lines_.append({
                                "a":a,
                                "b":b,
                                "m":points_[a]["obj"],
                                "n":points_[b]["obj"]
                                })
            module_points.append(points_)
            module_lines.append(lines_)



#outside_lines生成，连线！！！哈哈哈哈哈哈哈哈哈哈哈哈哈哈大快人心！！！！！！
outside_lines=[]
mark_point_ports=1
for m in range(0,len(module_points)):
    outside_port_type_=[]
    outside_port_type = []
    for each in module_points[m]:
        for i in range(0,len(each["sub"])):
            x = each["sub"][i]
            for y in modules[x].outside_port_:
                typey = outside_ports[y].type
                if typey not in outside_port_type_:
                    outside_port_type_.append(typey)
    for i in range(0,len(outside_port_type_)-1):
        for j in range(i,len(outside_port_type_)):
            if outside_port_type_[i] in outside_ports_rules[outside_port_type_[j]]:
                for n in range(0,len(module_points[m])):
                    outside_ports.append(outside_port({
                            "name":"point_port"+str(mark_point_ports),
                            "type":outside_port_type_[i],
                            "degree":outside_ports_degree[outside_port_type_[i]],
                            "father":-1,
                            "mother":(m,n),
                            "line_":[],
                            "position_x":0,
                            "position_y":0
                            }))
                    module_points[m][n]["outside_port_"].append(len(outside_ports)-1)
                    outside_ports.append(outside_port({
                            "name":"point_port"+str(mark_point_ports),
                            "type":outside_port_type_[j],
                            "degree":outside_ports_degree[outside_port_type_[j]],
                            "father":-1,
                            "mother":(m,n),
                            "line_":[],
                            "position_x":0,
                            "position_y":0
                            }))
                    module_points[m][n]["outside_port_"].append(len(outside_ports)-1)
                    
    for each in module_points[m]:
        for x in each["sub"]:
            for port_1 in modules[x].outside_port_:
                for port_2 in each["outside_port_"]:
                    port1=outside_ports[port_1]
                    port2=outside_ports[port_2]
                    if port1.type in outside_ports_rules[port2.type] and\
                    port2.type in outside_ports_rules[port1.type]:
                        if port1.degree>0:
                            outside_lines.append(outside_line({
                                    "start":port_1,
                                    "end":port_2
                                    }))
                        else:
                            outside_lines.append(outside_line({
                                    "start":port_2,
                                    "end":port_1
                                    }))
                        outside_ports[port_1].line_.append(len(outside_lines)-1)
                        outside_ports[port_2].line_.append(len(outside_lines)-1)
    
    for each_line in module_lines[m]:
        for a in module_points[m][each_line["a"]]["outside_port_"]:
            for b in module_points[m][each_line["b"]]["outside_port_"]:
                each_port_a = outside_ports[a]
                each_port_b = outside_ports[b]
                boolA=False
                boolB=False
                for c in modules[each_line["m"][0]].outside_port_:
                    each_port_c = outside_ports[c]
                    if each_port_a.type == each_port_c.type:
                        boolA = True
                        break
                for d in modules[each_line["m"][0]].outside_port_:
                    each_port_d = outside_ports[d]
                    if each_port_b.type == each_port_d.type:
                        boolB = True
                        break 
                if boolA and boolB:
                    if each_port_a.degree>0:
                        outside_lines.append(outside_line({
                                "start":a,
                                "end":b
                                }))
                    else:
                        outside_lines.append(outside_line({
                                "start":b,
                                "end":a
                                }))
                    outside_ports[a].line_.append(len(outside_lines)-1)
                    outside_ports[b].line_.append(len(outside_lines)-1)
    
#针对每个point，添加 inside_line
for each in module_points:
    for each_point in each:
        for i in range(0,len(each_point["outside_port_"])-1):
            for j in range(i,len(each_point["outside_port_"])):
                a = each_point["outside_port_"][i]
                b = each_point["outside_port_"][j]
                outside_port1 = outside_ports[a]
                outside_port2 = outside_ports[b]
                if outside_port1.type in \
                outside_ports_rules[outside_port2.type]:
                    if outside_port1.degree>0:
                        each_point["lines"].append({
                                "start":each_point["outside_port_"][i],
                                "end":each_point["outside_port_"][j],
                                })
                    else:
                        each_point["lines"].append({
                                "start":each_point["outside_port_"][j],
                                "end":each_point["outside_port_"][i],
                                })
                    position_x=0
                    position_y=0
                    count_x=0
                    count_y=0
                    for m in outside_port1.line_:
                        portId = outside_lines[m].start if outside_lines[m].start!=a\
                        else outside_lines[m].end
                        if outside_ports[portId].position_x!=0 or \
                        outside_ports[portId].position_y!=0:
                            position_x += outside_ports[portId].position_x
                            position_y += outside_ports[portId].position_y
                            count_x += 1
                            count_y += 1
                    for n in outside_port2.line_:
                        portId = outside_lines[n].start if outside_lines[n].start!=b\
                        else outside_lines[n].end
                        if outside_ports[portId].position_x!=0 or \
                        outside_ports[portId].position_y!=0:
                            position_x += outside_ports[portId].position_x
                            position_y += outside_ports[portId].position_y
                            count_x += 1
                            count_y += 1
                    outside_port1.position_x = position_x/count_x if count_x!=0 else 0
                    outside_port1.position_y = position_y/count_y if count_y!=0 else 0
                    outside_port2.position_x = position_x/count_x if count_x!=0 else 0#+1
                    outside_port2.position_y = position_y/count_y if count_y!=0 else 0


#绘制逻辑图
G = nx.DiGraph()      
for each_line in outside_lines:
    from_port = each_line.start
    if outside_ports[from_port].father!=-1:
        A = modules[outside_ports[from_port].father].name
    else:
        A = str(outside_ports[from_port].mother)
    end_port = each_line.end
    if outside_ports[end_port].father!=-1:
        B = modules[outside_ports[end_port].father].name
    else:
        B = str(outside_ports[end_port].mother)
    G.add_edge(A,B)
#print("输出全部节点：{}".format(G.nodes()))
#print("输出全部边：{}".format(G.edges()))
#print("输出全部边的数量：{}".format(G.number_of_edges()))
nx.draw(G,cmap = plt.get_cmap('jet'),with_labels=True,node_size=200,node_color='#307aff',edge_color='g')  
plt.show()
print('--------------------------------------------------------')
print('--------------------------------------------------------')




#需要的输出















################################################################
#绘图准备
doc = ezdxf.new('R2000', setup=True)
msp = doc.modelspace()
doc.styles.new('new', dxfattribs={'font' : 'Adobe Fangsong Std'})
flag = doc.blocks.new(name='Module')
flag.add_lwpolyline([(0, 0), (10, 0), (10, 4), (0, 4),(0,0)])#宽10，高4
#简单算法（以后要改，要根据内部连线和外部连线的综合状况，来布置outside_port的位置）
    
#doc.add_line()
#msp.add_blockref('GSHP',(0,0), dxfattribs={})
for each in modules:
    msp.add_blockref('Module',(each.position_x,each.position_y), dxfattribs={})
    msp.add_text(each.name,
                 dxfattribs={
                     'style': 'new',
                     'height': 0.35}
                 ).set_pos((each.position_x+4,each.position_y+1),\
                          (each.position_x+6,each.position_y+1), align='ALIGNED')
  
'''    
for each_ in module_points:
    for each in each_:
        for each_line in each["lines"]:
            start = outside_ports[each_line["start"]]
            end = outside_ports[each_line["end"]]
            msp.add_line((start.position_x,start.position_y),(end.position_x,end.position_y))
            print((start.position_x,start.position_y),(end.position_x,end.position_y))
'''
            
for each_line in outside_lines:
    start = outside_ports[each_line["start"]]
    end = outside_ports[each_line["end"]]
    msp.add_line((start.position_x,start.position_y),(end.position_x,end.position_y))
    

doc.saveas("output.dxf")
    


                
            
                







               
            


