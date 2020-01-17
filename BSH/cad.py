#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 16:56:51 2020

@author: xiaoqiqi
"""

import ezdxf

doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'

msp = doc.modelspace()  # add new entities to the modelspace
msp.add_line((0, 0), (10, 0))  # add a LINE entity
doc.saveas('line.dxf')