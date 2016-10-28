#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import re
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
#from decimal import *
#getcontext().prec = 2
date = raw_input('Enter the date you want to visualize (eg.201606): ')
monthBalancePath = './ergebnisse/ergebnis'+date+'.csv'
monthBalanceDF = pd.read_csv(monthBalancePath,sep=';')
#rulesPath = "./regeln.csv"
#rulesDF = pd.read_csv(rulesPath, sep=";")

result = pd.DataFrame(columns=['Kategorie','Betrag'])
result['Kategorie'] = ['Einkommen','Lebensmittel','Verkehr','Personal','Kommunikation','Haus','Kleidung','Spende','Anders','Sozial','Rest']
result.Betrag = 0
rest = 0
for i in result.index:
    for j in monthBalanceDF.index:
        if result.loc[i,'Kategorie'] == monthBalanceDF.loc[j,'Kategorie']:
            result.loc[i,'Betrag'] += float(monthBalanceDF.loc[j,'Betrag'])

for i in result.index:
    rest += float(result.loc[i,'Betrag'])

result.loc[10,'Betrag'] = rest

pp = PdfPages('./ergebnisse/output'+date+'.pdf')
#result.plot(how = 'table')
plt.figure()
bild = result.plot(kind='barh',fontsize = 7)
ylabels = result['Kategorie']
bild.set_yticklabels(ylabels)
for i, v in enumerate(result['Betrag']):
        bild.text(v + 3, i + .2, str(v), color='red', fontweight='bold')
#ylabels = result['Betrag']
#rects = bild.patches
#for rect, ylabel in zip(rects,ylabels):
#    height = rect.get_height()
#    bild.text(rect.get_x() + rect.get_height()/2,height+5,ylabel,ha='center',va='bottom')
pp.savefig()
pp.close()
