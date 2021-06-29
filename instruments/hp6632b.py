# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 01:55:09 2021

@author: nicolas

6632B/66332A SCPI Commands

# Example:

#     # Print Device ID
#     print(psu_vdda.query("*IDN?"))
#     print(psu_vddd.query("*IDN?"))

#     # 66332A: Set current range low, ACDC and 1.8V with 10mA current limit
#     psu_vdda.write("SENS:CURR:RANG 0.019")
#     psu_vdda.write("SENS:CURR:DET ACDC")
#     psu_vdda.write("VOLT 1.8;CURR 0.01")

#     # 6632B: Set current range low and 1.8V with 20mA current limit
#     psu_vddd.write("SENS:CURR:RANG 0.019")
#     psu_vddd.write("VOLT 1.8;CURR 0.02")

#     # Turn output on
#     psu_vddd.write("OUTP ON")
#     psu_vdda.write("OUTP ON")

"""


class hp6632b:
    def __init__(self, inst):
        self.inst = inst
        self.hp66332A = False

    def setHandle(self, handle):
        self.inst = handle

    def set66332A(self):
        self.hp66332A = True

    def getID(self):
        self.inst.query("*IDN?")

    def setVoltage(self, voltage: float):

        if 0 <= voltage <= 20:
            self.inst.write("VOLT " + str(voltage))

    def setCurrent(self, current: float):

        if 0 <= current <= 5.0:
            self.inst.write("CURR " + str(current))

    def setCurrentRangeLow(self, low: bool):

        if low:
            self.inst.write("SENS:CURR:RANG 0.019")
        else:
            self.inst.write("SENS:CURR:RANG 1")

    def setOutputON(self, on: bool):
        if on:
            self.inst.write("OUTP ON")
        else:
            self.inst.write("OUTP OFF")

    def setMode(self, mode: str):
        validModes = {'ACDC', 'DC'}

        if mode in validModes:
            self.inst.write("SENS:CURR:DET " + mode)

    def getVoltage(self):

        return float(self.inst.query("MEAS:VOLT?").rstrip("\n"))

    def getCurrent(self):

        return float(self.inst.query("MEAS:CURR?").rstrip("\n"))
