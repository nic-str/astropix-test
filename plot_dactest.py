# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:58:50 2021

@author: nicolas
"""


import pandas as pd

import matplotlib.pyplot as plt


#print(pd.__version__)
plt.rcParams["figure.dpi"] = 144

filename='newchip2_dac'


headers = ['DAC_name', 'DAC_value', 'VDDA', 'IDDA', 'VDDD', 'IDDD', 'IRB']
df = pd.read_csv(f'csv/{filename}.csv', sep=',', names=headers, header=1)

plt.figure()
df.set_index('DAC_value', inplace=True)
df['IDDA'] = 1000 * df['IDDA']
ax = df.groupby('DAC_name')['IDDA'].plot(legend=True,title='DAC Linearity',figsize=(10,7))
plt.xlabel('DAC Value')
plt.ylabel('I(VDDA), mA')
#plt.show()
plt.savefig(f'plots/{filename}.png')