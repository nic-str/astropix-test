# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:58:50 2021

@author: nicolas
"""


import pandas as pd

import matplotlib.pyplot as plt


#print(pd.__version__)
plt.rcParams["figure.dpi"] = 144

filename='inj_chip1_amp2_vn1'


headers = ['Vinj', 'aver', 'dev']
df = pd.read_csv(f'csv/{filename}.csv', sep=',', names=headers, header=1)

plt.figure()
df.set_index('Vinj', inplace=True)
df['aver'] = 1000 * df['aver']
df['dev'] = 1000 * df['dev']
ax = df['aver'].plot(legend=True,title='Injection VN=2',figsize=(10,7))
#ax = df['dev'].plot(secondary_y=True, color='k', marker='o')
ax = df.plot(legend=False,secondary_y=['dev'], marker='.')

ax.set_xlabel('Vinj, V')
ax.set_ylabel('Vsfout2, mV')
ax.right_ax.set_ylabel('Noise, mVrms')
#plt.xlabel('DAC Value')
#plt.ylabel('I(VDDA), mA')
#plt.show()
plt.suptitle(f'{filename}')
plt.savefig(f'plots/{filename}.png')