# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:58:50 2021

@author: nicolas
"""


import pandas as pd

import matplotlib.pyplot as plt


#print(pd.__version__)
plt.rcParams["figure.dpi"] = 144

filename='ui_test'


headers = ['U', 'I','x1','x2','x3','x4']
df = pd.read_csv(f'csv/{filename}.csv', sep=',', names=headers, header=1)

plt.figure()
df.set_index('U', inplace=True)
df['I'] = 1e6 * df['I']
ax = df['I'].plot(legend=True,title='AstroPix2 Breakdown Voltage new Guardring',figsize=(10,7))

ax.set_xlabel('HV, V')
ax.set_ylabel('Current, uA')

plt.suptitle(f'{filename}')
plt.savefig(f'plots/{filename}.png')