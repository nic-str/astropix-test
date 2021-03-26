# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 12:08:16 2021

@author: nicolas
"""

import numpy
import pyvisa
import time
import csv

from datetime import datetime

from asicconfig_http import asicconfig_http

from instruments.mso5000 import mso5000
from instruments.hp6632b import hp6632b
from instruments.k236 import k236

enable_scope = True
enable_psu = False
enable_smu = False

path_screenshots = 'screenshots/'

# DACs to test
test_dacs={"vn1","vn2", "vnfoll", "vncomp"}

# Visa open resourcemanager
rm = pyvisa.ResourceManager()
#print(rm.list_resources())

# Visa open devices
if enable_psu:
    psu1 = rm.open_resource('GPIB::4::INSTR', open_timeout=1000)   # 66332A
    psu2 = rm.open_resource('GPIB::5::INSTR', open_timeout=1000)   # 6632B

if enable_scope:
    mso1 = rm.open_resource('TCPIP::192.168.1.10::INSTR', open_timeout=1000)

if enable_smu:
    smu1 = rm.open_resource('GPIB::24::INSTR', open_timeout=1000)   # K236

# PSU Setup
if enable_psu:
    psu_vdda = hp6632b(psu1)
    psu_vdda.setCurrentRangeLow(True)
    psu_vdda.setVoltage(1.8)
    psu_vdda.setCurrent(0.01)
    
    psu_vddd = hp6632b(psu2)
    psu_vddd.setCurrentRangeLow(True)
    psu_vddd.setMode('ACDC')
    psu_vddd.setVoltage(1.8)
    psu_vddd.setCurrent(0.02)
    
    print("PSU setup done")

# SMU Setup
if enable_smu:
    smu = k236(smu1)
    smu.setMode(0, 0)
    smu.setBias(-50, 3, 0)
    smu.setCompliance(500E-6,7)
    smu.setTriggerEnable(True)
    smu.setIntegrationTime(3)
    smu.setFilter(5)
    smu.setTrigger()
    
    print("SMU setup done")

# Scope Setup
if enable_scope:
    mso = mso5000(mso1)
    mso.getScreenshot('test.png')
    
    print("Scope setup done")

#Enable Outputs
if enable_scope & enable_psu & enable_smu:
    psu_vdda.setOutputON(True)
    psu_vddd.setOutputON(True)
    time.sleep(1)
    smu.setOperate(True)
    
    print("Outputs enabled")

psu_vdda_volts = 0
psu_vdda_amps = 0
psu_vddd_volts = 0
psu_vddd_amps = 0

csv_list = []



# Test DAC Linearity
if False:
    # Output CSV filename
    filename = input("Input the Filename: ")
    
    # Create Config Object
    config = asicconfig_http()
    
    #Iterate trough DACs in list
    for dac_name in test_dacs:
        
        dac_value = 0
    
        #Reset all DACs to 5
        for dac_name2 in test_dacs:
            config.setDac(dac_name2, 5)
        
        while dac_value < 64:
    
            #Set DAC und Update Asic via http
            config.setDac(dac_name, dac_value)
            config.updateAsic()
    
            # 5s to settle
            time.sleep(5)
    
            # Read Voltage and Current from PSUs via GPIB
            psu_vdda_amps = psu_vdda.getCurrent()
            psu_vddd_amps = psu_vddd.getCurrent()     
            psu_vdda_volts = psu_vdda.getVoltage()
            psu_vddd_volts = psu_vddd.getVoltage()
            
            # Read Current from SMU via GPIB
            smu_amps = smu.getMeasureDC()
    
            #Print to Console
            print("DAC: {}\n\
                DAC_value: {}\n\
                V(Vdda): {} V\n\
                V(Vddd): {} V\n\
                I(Vdda): {} mA\n\
                I(Vddd): {} mA\n\
                I(SMU): {} nA\n".format(
                    dac_name,
                    dac_value,
                    round(psu_vdda_volts,3),
                    round(psu_vddd_volts,3),
                    round(psu_vdda_amps * 1000,3),
                    round(psu_vddd_amps * 1000,3),
                    round(smu_amps * 1e+09,4)),
                sep='')
    
            #Append to list for csv output
            csv_list.append([dac_name,
                             dac_value,
                             psu_vdda_volts,
                             psu_vdda_amps,
                             psu_vddd_volts,
                             psu_vddd_amps,
                             smu_amps])
    
            dac_value = dac_value + 5
    
    #Convert list to numpy array
    csv_array = numpy.array(csv_list)
    
    # Write np array to csv
    header = "DAC_name,DAC_value,VDDA,IDDA,VDDD,IDDD,IRB"
    numpy.savetxt('csv/{}.csv'.format(filename),
                  csv_array,
                  delimiter=",",
                  fmt='%s',
                  header=header)

# Create Histogram
if False: 
    # Set trigger on injection Channel
    mso.setTrigger('edge', 'ac', 'normal', 'negative', 0.10, 'channel3')
    
    #Setup Vmax Measurement
    mso.setStatisticsItem('vmax','chan1')
    
    #Setup Histogram
    mso.setHistogram(1, 'meas', 'chan1')
    
    #Reset statistics
    mso.setStatisticsReset()
    mso.setHistogramReset()
    
    #Setup Measure Statistics to monitor cnt; Histogram is 3x slower, than normal Measurement
    i=0
    cnt=0
    
    while i<3:
        time.sleep(10)
        cnt=float(mso.getStatisticsItem('cnt','vmax','chan1'))
        if cnt > 50:
            i = i+1
            mso.setStatisticsReset()
    
    #DEBUG
    stat_max = mso.getStatisticsItem('max','vmax','chan1')
    stat_min = mso.getStatisticsItem('min','vmax','chan1')
    stat_dev = mso.getStatisticsItem('dev','vmax','chan1')
    stat_avg = mso.getStatisticsItem('dev','vmax','chan1')
    
    
    print(f'Max: {stat_max}\nMin: {stat_min}\nDev: {stat_dev}\nAvg: {stat_avg}\n')
    mso.getScreenshot('test_histogram.png')
        
    # Todo: CSV Output

# Test SFOUT    
if True:
    config = asicconfig_http()
    
    
    
    #Setup Vmax Measurement
    mso.setStatisticsItem('vmax','chan1')
    
    filename = input("Input the Filename: ")
    header = "Vinj,aver,dev"
    csv_array=[]
    numpy.savetxt('csv/{}.csv'.format(filename),
                  csv_array,
                  delimiter=",",
                  fmt='%s',
                  header=header)
    
    injectionvoltage=0.1
    
    dev=0
    avg=0
    max=0
    csv_list=[]
    
    mso.setChannelProbe(1,1)
    mso.setChannelProbe(10,2)
    mso.setChannelOptions('100M', 'AC', 1)
    mso.setChannelOptions('100M', 'DC', 2)
    
    mso.setChannelScale(0.01,1)
    mso.setChannelScale(0.05,2)
    # Set trigger on injection Channel
    mso.setTriggerEdge('ac', 'normal', 'negative', 0.05, 'channel2')
    
    while injectionvoltage <= 1.8:
        config.startInjection(injectionvoltage, 500, 100, 300)
        
        
        mso.setStatisticsReset()
        time.sleep(10)
        maximum=float(mso.getStatisticsItem('max','vmax','chan1'))
        mso.setChannelScale(maximum/4,1)
        
        # Sample 5s to adjust scale
        mso.setStatisticsReset()
        while float(mso.getStatisticsItem('cnt','vmax','chan1')) < 500:
            time.sleep(5)
        
            
        dev=float(mso.getStatisticsItem('dev','vmax','chan1'))
        avg=float(mso.getStatisticsItem('aver','vmax','chan1'))
        
        csv_list=[injectionvoltage,avg,dev]
        #line=numpy.array(csv_list)
        
        with open('csv/{}.csv'.format(filename),'a', newline='') as fd:
            csv_writer = csv.writer(fd)
            csv_writer.writerow(csv_list)
            #fd.write(str(csv_list).strip('[]'))
        
        
        injectionvoltage=round(injectionvoltage+0.05,2)
    
    
    

    



