# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 12:08:16 2021

@author: nicolas
"""

import numpy
import pyvisa
import time
import csv

from asicconfig_http import asicconfig_http

from instruments.mso5000 import mso5000
from instruments.hp6632b import hp6632b
from instruments.k236 import k236
from instruments.b2901a import b2901a

rm = pyvisa.ResourceManager()
inst = rm.open_resource('GPIB::12::INSTR', open_timeout=1000)

smu = b2901a(inst)

print(smu.getID())

inst.write("")