# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 12:08:16 2021

@author: nicolas
"""

#import numpy
import pyvisa
import time
import csv

from instruments.b2901a import b2901a

filename = "ui_test"

voltage = -10
voltage_stop = -200
voltage_step = -1

settling_time = 5

rm = pyvisa.ResourceManager()
print(rm.list_resources())

smu = b2901a(rm.open_resource('GPIB0::23::INSTR', open_timeout=1000))

print(smu.getID())

smu.setMode("VOLT")
smu.setFunc("CURR")
smu.setLimit(-5e-6)
smu.setNPLC(200)

smu.setVal(0)


with open(f'csv/{filename}.csv', 'w', newline='') as outcsv:
    csv_writer = csv.DictWriter(outcsv, fieldnames = ['U', 'I','x1','x2','x3','x4'])
    csv_writer.writeheader()

smu.enableOut(True)

while voltage >= voltage_stop:
    smu.setVal(voltage)

    voltage += voltage_step
    time.sleep(settling_time)

    readList = smu.getVal().split(",")
    print(readList)

    with open(f'csv/{filename}.csv', 'a', newline='') as outcsv:
        csv_writer = csv.writer(outcsv)
        csv_writer.writerow(readList)

smu.enableOut(False)
smu.setVal(0)
