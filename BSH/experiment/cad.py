#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 16:56:51 2020

@author: xiaoqiqi
"""

import ezdxf

doc = ezdxf.new('R2000', setup=True)

################################################################

doc.styles.new('new', dxfattribs={'font' : 'Adobe Fangsong Std'})

################################################################

flag = doc.blocks.new(name='GSHP')
flag.add_lwpolyline([(0, 0), (10, 0), (10, 4), (0, 4),(0,0)])
flag.add_line((-2,1),(0,1))
flag.add_line((-2,3),(0,3))
flag.add_line((10,1),(12,1))
flag.add_line((10,3),(12,3))
flag.add_lwpolyline([(0,2),(10,2)])
flag.add_text("GSHP",
             dxfattribs={
                 'style': 'new',
                 'height': 0.35}
             ).set_pos((2, 5),(8,5), align='ALIGNED')

flag = doc.blocks.new(name='BUMP')
flag.add_lwpolyline([(-2,0),(0,0),(1.732,1),(1.732,-1),(0,0)])
flag.add_line((2.31,0),(4.31,0))
flag.add_circle((1.1547, 0), 1.1547)





################################################################


msp = doc.modelspace()
msp.add_text("哈哈哈",
             dxfattribs={
                 'style': 'new',
                 'height': 0.35}
             ).set_pos((8, 5),(8,5), align='ALIGNED')

msp.add_blockref('GSHP',(0,0), dxfattribs={})

msp.add_blockref('BUMP',(24,8), dxfattribs={})
msp.add_blockref('BUMP',(24,12), dxfattribs={})

doc.saveas("abc.dxf")
