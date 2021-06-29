# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:47:57 2021

@author: nicolas

MSO5000 SCPI Commands

partially from: https://gitlab.com/thmjpr/mso5000-gui
"""

class mso5000:
    
    def __init__(self, inst):
        self.inst = inst
        self.path_screenshots='screenshots/'
        
    def setHandle(self, inst):
        self.inst=inst
    
    def setScreenshotPath(self, path):
        self.path_screenshots=path
    
    def getScreenshot(self, filename='rigol.png'):
        # Request Binary Data and write to Buffer
        buf = self.inst.query_binary_values(':DISP:DATA? ON,0,PNG', datatype='B')
    
        # Write Buffer to PNG
        with open(self.path_screenshots+filename, 'wb') as f:
            print('Capturing screen to', self.path_screenshots+filename)
            f.write(bytearray(buf))
    
    #Channel settings  
    def setChannelDisplay(self, channel=1, enable=1):
        self.inst.write(':CHANnel'+str(channel)+':DISPlay '+str(enable))
        
    def setChannelScale(self, scale="1.000", channel=1):
        self.inst.write(':channel' + str(channel) + ':scale ' + str(scale))

   
    def setChannelOptions(self, BWlimit='OFF', coupling='DC', channel=1):
        validBW = {'20M', '100M', '200M', 'OFF'}
        
        if BWlimit in validBW:
            self.inst.write(':channel' + str(channel) + ':bwlimit ' + BWlimit)
    
        validCouple = {'AC', 'DC'}
        
        if coupling in validCouple:
            self.inst.write(':channel' + str(channel) + ':coupling ' + coupling)
        #Channel settings
    
    def setChannelProbe(self, probe=1,channel=1):
        validProbe = {1, 10}
        
        if probe in validProbe:
            self.inst.write(':channel' + str(channel) + ':probe ' + str(probe))
            
    #Timebase
    #modes Main, Xy, Roll
    def setTimebaseMode(self, mode='main'):
        self.inst.write(':timebase:mode ' + mode)

    #modes: center, lb, rb, trig, user
    def setTimebasePosition(self, ref='center'):
        self.inst.write(':timebase:hreference:mode ' + ref)

    def setTimebase(self, timebase=0.001):
        self.inst.write(':timebase:main:scale ' + str(timebase))  #f'{numvar:.9f}'

    #Trigger
    #mode: edge, pulse, slope, video, pattern, duration, timeout, runt, window, delay, setup, nedge, ...
    #coupling: ac, dc, lfreject, hfreject
    #sweep: auto, normal, single
    #holdoff:
    #source: channel1, channel2, D0, etc..
    def setTriggerEdge(self, coupling='ac', sweep='normal', slope='positive', level=0.00, source='channel1'):
        self.inst.write(':trigger:mode edge')
        self.inst.write(':trigger:sweep ' + sweep)
        self.inst.write(':trigger:coupling ' + coupling)
        self.inst.write(':trigger:edge:source ' + source)
        self.inst.write(':trigger:edge:slope ' + slope)
        self.inst.write(':trigger:edge:level ' + str(level))

    #display
    def displayClear(self):
        self.inst.write(':display:clear')

    #read values
    def getMeasAmplitude(self, channel=1):
        try:
            return float(self.inst.query(':measure:item? vamp,channel' + str(channel)).rstrip())  #request measurement, convert to float
        except TypeError:
            return 0
    
    def getMeasVmax(self, channel=1):
        try:
            return float(self.inst.query(':measure:item? vmax,channel' + str(channel)).rstrip())  #request measurement, convert to float
        except TypeError:
            return 0

    def getMeasFrequency(self, channel=1):
        try:
            return float(self.inst.query(':measure:item? freq,channel' + str(channel)).rstrip())
        except TypeError:
            return 0

    def getImpedance(self, channel=1):
        #if string == "OMEG" or "FIFT"
        #return Impedance.FiftyOhm
        pass

    def setupMeasPhase(self, channelA=1, channelB=2):       #can also use digital or math channels
        self.inst.write(':measure:setup:psa chan' + str(channelA))
        self.inst.write(':measure:setup:psb chan' + str(channelB))
        #self.inst.write(':measure:setup:dsa chan' + str(channelA))
        #self.inst.write(':measure:setup:dsb chan' + str(channelB))

    def getMeasPhase(self, channelA=1, channelB=2):
        return float(self.inst.query(
            ':measure:item? rrphase,channel' + str(channelA) + ',channel' + str(channelB)).rstrip())  #request measurement, convert to float
        #rrPhase, rfPhase frphase ffphase? which one

    def getOutputState(self, channel="1"):
        resp = self.inst.query(":source:OUTP" + channel + ":state?")
        resp = resp.rstrip()
        
        if resp == "1":
            return True
        
        return False

    #Read waveform data
    #set waveform source channel
    def waveSource(self, channel='channel1'):
        self.checkSourceValid(channel)
        self.inst.write(':waveform:source ' + channel)

    #mode: normal, maximum, raw (must be in stop mode)
    #format: word, byte, ascii (comma separated scientific notation)
    def waveDataFormat(self, mode='normal', waveDataformat='byte', points=1000):
        self.inst.write(':waveform:mode ' + mode)
        self.inst.write(':waveform:format ' + waveDataformat)
        self.inst.write(':waveform:format ' + str(points))

    def getWaveData(self):
        pass
    
    def setHistogram(self, enable, histogramtype, sourcechannel, size = 3, statistics = 1):
        
        self.inst.write(':histogram:display ' + str(enable))
        
        validType = {'horizontal', 'vertical', 'meas'}
        if type in validType:
            self.inst.write(':histogram:type ' + histogramtype)
        
        self.inst.write(':histogram:source chan' + sourcechannel)
        
        self.inst.write(':histogram:height ' + str(size))
        
        self.inst.write(':histogram:static ' + str(statistics))
        
    def setHistogramReset(self):
        """ Reset Histogram Statistics"""
        
        self.inst.write(':HISTogram:RESet')
        
    def setMeasureItem(self, item, source):
        """ Set Statistics
        
        :param item: VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|VRMS|OVERshoot|PREShoot|MARea|MPARea|PERiod|FREQuency|RTIMe|FTIMe|PWIDth|NWIDth|PDUTy|NDUTy|TVMax|TVMin|PSLewrate|NSLewrate|VUPPer|VMID|VLOWer|VARiance|PVRMs|PPULses|NPULses|PEDGes|NEDGes|RRDelay|RFDelay|FRDelay|FFDelay|RRPHase|RFPHase|FRPHase|FFPHase
        :param source: D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15|CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH1|MATH2|MATH3|MATH4
        """
        
        self.inst.write(f':MEASure:ITEM {item},{source}')
        
    def getMeasureItem(self, item, source):
        """ Set Statistics
        
        :param item: VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|VRMS|OVERshoot|PREShoot|MARea|MPARea|PERiod|FREQuency|RTIMe|FTIMe|PWIDth|NWIDth|PDUTy|NDUTy|TVMax|TVMin|PSLewrate|NSLewrate|VUPPer|VMID|VLOWer|VARiance|PVRMs|PPULses|NPULses|PEDGes|NEDGes|RRDelay|RFDelay|FRDelay|FFDelay|RRPHase|RFPHase|FRPHase|FFPHase
        :param source: D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15|CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH1|MATH2|MATH3|MATH4
        """
        
        return self.inst.query(f':MEASure:ITEM? {item},{source}').rstrip("\n")
    
    def setStatisticsItem(self, item, source):
        """ Set Statistics
        
        :param item: VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|VRMS|OVERshoot|PREShoot|MARea|MPARea|PERiod|FREQuency|RTIMe|FTIMe|PWIDth|NWIDth|PDUTy|NDUTy|TVMax|TVMin|PSLewrate|NSLewrate|VUPPer|VMID|VLOWer|VARiance|PVRMs|PPULses|NPULses|PEDGes|NEDGes|RRDelay|RFDelay|FRDelay|FFDelay|RRPHase|RFPHase|FRPHase|FFPHase
        :param source: D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15|CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH1|MATH2|MATH3|MATH4
        """
        
        self.inst.write(f':MEASure:STATistic:ITEM {item},{source}')
        
    def setStatisticsReset(self):
        """ Reset Statistics"""
        
        self.inst.write(':MEASure:STATistic:RESet')
        
    def getStatisticsItem(self, itemtype, item, source):
        """ Get Statistics
        
        :param type: MAXimum|MINimum|CURRent|AVERages|DEViation|CNT
        :param item: VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|VRMS|OVERshoot|PREShoot|MARea|MPARea|PERiod|FREQuency|RTIMe|FTIMe|PWIDth|NWIDth|PDUTy|NDUTy|TVMax|TVMin|PSLewrate|NSLewrate|VUPPer|VMID|VLOWer|VARiance|PVRMs|PPULses|NPULses|PEDGes|NEDGes|RRDelay|RFDelay|FRDelay|FFDelay|RRPHase|RFPHase|FRPHase|FFPHase
        :param source: D0|D1|D2|D3|D4|D5|D6|D7|D8|D9|D10|D11|D12|D13|D14|D15|CHANnel1|CHANnel2|CHANnel3|CHANnel4|MATH1|MATH2|MATH3|MATH4
        """
        
        return self.inst.query(f':MEASure:STATistic:ITEM? {type},{itemtype},{source}').rstrip("\n")
        
        
