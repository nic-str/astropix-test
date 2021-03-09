# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 02:18:48 2021

@author: nicolas

Keithley 236 Commands 

Example:
    # Get Model Number and Firmware
    print(smu.query("U0X"))

    # Source Voltage dc
    smu.write("F0,0X")

    # Voltage Range
    smu.write("B-50,3,0X")

    # Current Range: 500umA Compliance, 10mA range
    smu.write("L500E-6,7X")

    # Enable Trigger
    smu.write("R1X")

    # Enable Output
    smu.write("N1X")

    # Trigger
    smu.write("H0X")

    # Set Integration Linecycle 50Hz and 32 Readings Filter
    smu.write("S3P5X")
    
    #Get Data
    smu.query("G4,0,0X")
"""


class k236:
    def __init__(self, inst):
        self.inst = inst
    
    def getID(self):
        """Get Device ID"""
        
        return self.inst.query("U0X")
        
    def setMode(self, source: int, function: int):
        """Set Mode
        
        :param source: V=0 I=1
        :param function: DC=0 Sweep=1
        """
        
        if ((source == 0) | (source == 1)) & ((function == 0) | (function == 1)):
            self.inst.write(f'F{source},{function}X')
    
    def setBias(self, level: float, range: int, delay: int):
        """Set Bias 
        
        :param level: I/V
        :param range: 10^(range-1) nA / 1.1V, 11V, 110V 
        :param delay: 0-65000 ms
        """
       
        if ((level <= 110) & (level >= -110)):
            if ((range < 10) & (range >= 10)):
                if ((delay <= 65000) & (delay >= 0)):
                    self.inst.write(f'B{level},{range},{delay}X')
                    
    def setCompliance(self, level: float, range: int):
        """Set Compliance Level 
        
            :param level: I/V
            :param range: 10^(range-1) nA / 1.1V, 11V, 110V
        """
        
        if ((level <= 110) & (level >= -110)):
            if ((range < 10) & (range >= 10)):
                self.inst.write(f'L{level},{range}X')
                
    def setTriggerEnable(self, enable: bool):
        """Enable Input/Output Trigger"""
        
        if enable:
            self.inst.write("R1X")
        else:
            self.inst.write("R0X")
    
    def setIntegrationTime(self, period: int):
        """Set Integration Time 
        
        :param period: 0=416us, 1=4ms, 2=Linecycle 60Hz, 3=Linecycle 50Hz
        """
        
        if ((period < 4) & (period >= 0)):
            self.inst.write(f'S{period}X')
            
    def setFilter(self, number: int):
        """Set number of readings averaged 
        
        :param number: averaged samples = 2^number
        """
        
        if ((number < 6) & (number >= 0)):
            self.inst.write(f'P{number}X')
            
    def setOperate(self, enable: bool):
        """Enable output True/False"""
        
        if enable:
            self.inst.write('N1X')
        else:
            self.inst.write('N0X')
            
    def setTrigger(self):
        """Send immediate Trigger"""
        
        self.inst.write("H0X")
        
    def getData(self, items: int, format: int, lines: int):
        """Get Data
        
        :param item: 0=no items, 1=source value, 2= Delay value, 4=Measure value, 8=Time value
        :param format: 0 = ASCII data with prefix and suffix 1 = ASCII data with prefix, no suffix 2 = ASCII data, no prefix or suffix 3 = HP binary data 4 = IBM binary data
        :param lines: 0 = One line of de data per talk 1 = One line of sweep data per talk 2 = All lines of sweep data per talk
        """
        
        validItems={0,1,2,4,8}
        
        if items in validItems:
            if ((format < 5) & (format >= 0)):
                if ((lines < 3) & (lines >= 0)):
                   return self.inst.query(f'G{items},{format},{lines}X')
    
    def getMeasureDC(self, format = 2, lines = 0):
        """Get DC Data
        
        :param format: 0 = ASCII data with prefix and suffix 1 = ASCII data with prefix, no suffix 2 = ASCII data, no prefix or suffix 3 = HP binary data 4 = IBM binary data
        :param lines: 0 = One line of data per talk 1 = One line of sweep data per talk 2 = All lines of sweep data per talk
        """
        
        if ((format < 5) & (format >= 0)):
            if ((lines < 3) & (lines >= 0)):
               return float(self.inst.query(f'G4,{format},{lines}X').rstrip("\n"))
