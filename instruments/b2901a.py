# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 01:55:09 2021

@author: nicolas

B2901A SCPI Commands


"""

class b2901a:

    def __init__(self, inst):
        self.inst = inst
        self.mode = "VOLT"

    def setHandle(self, handle):
        self.inst = handle

    def getID(self):
        return self.inst.query("*IDN?")

    def setMode(self, mode: str):
        validModes = {'VOLT', 'CURR'}

        if mode in validModes:
            self.inst.write(":SOUR:FUNC:MODE " + mode)
            self.mode = mode

    def setVal(self, value: float):
        if self.mode == "VOLT":
            if not -210 <= value <= 210:
                value = 0
        elif self.mode == "CURR":
            if not -3 <= value <= 3:
                value = 0
       
        self.inst.write(":SOUR:"+self.mode + " " + str(value))

    def setFunc(self, function: str):

        validFunctions = {'VOLT', 'CURR', 'RES'}

        if function in validFunctions:
            self.inst.write(":SENS:FUNC " + function)

    def setNPLC(self, nplc: float):
        if 0 < nplc <= 200:
            self.inst.write(":SENS:FUNC:NPLC " + str(nplc))

    def setLimit(self, value: float):
        if self.mode == "VOLT":
            limitmode = "CURR"
        elif self.mode == "CURR":
            limitmode = "VOLT"

        self.inst.write(":SENS:" + limitmode + ":PROT " + str(value))

    def enableOut(self, enable: bool):
        if enable:
            enstring = "ON"
        else:
            enstring = "OFF"

        self.inst.write(":OUTP " + enstring)

    def getVal(self):

        return self.inst.query(":MEAS?").rstrip("\n")

    def getFunc(self):

        return self.inst.query(":MEAS:FUNC?").rstrip("\n")
