# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 12:08:16 2021

@author: nicolas
"""

#import numpy
import pyvisa
import time
import csv

#sfrom asicconfig_http import asicconfig_http

from instruments.mso5000 import mso5000
from instruments.hp6632b import hp6632b
from instruments.k236 import k236
from instruments.b2901a import b2901a

filename = "ui_test"

rm = pyvisa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource('GPIB0::23::INSTR', open_timeout=1000)

smu = b2901a(inst)

print(smu.getID())

smu.setMode("VOLT")
smu.setFunc("CURR")
smu.setLimit(-5e-6)
smu.setNPLC(200)

smu.setVal(-1)

voltage = -10
voltage_step = -1

smu.enableOut(True)

while voltage >= -200:
    smu.setVal(voltage)

    voltage = voltage + voltage_step
    time.sleep(5)

    readVal = smu.getVal().rstrip("\n")

    readList = readVal.split(",")
    print(readList)

    with open('csv/{}.csv'.format(filename),'a', newline='') as fd:
        csv_writer = csv.writer(fd)
        csv_writer.writerow(readList)

smu.enableOut(False)
smu.setVal(0)

#inst.write("")