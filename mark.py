#!/usr/bin/env python
# encoding: utf-8

import re
import pandas as pd
date = raw_input('Enter the date you want to analyse (eg.201606): ')
amazonPath = "./data/Kreditkartenabrechnung"+date+'.csv'
giroPath = "./data/Girokonto"+date+".csv"
visaPath = "./data/Visacomdirect"+date+".csv"
#amazonPath = "./data/Kreditkartenabrechnung-2016-06-23.csv"
#giroPath = "./data/Girokonto201606.csv"
#visaPath = "./data/Visacomdirect201606.csv"
# clean the data
amazonDF = pd.read_csv(amazonPath, sep=';')
amazonDF.columns = ['Kartennummer','Buchungsdatum','Kaufdatum','Umsatz','Fremd','Kurs','Betrag']
amazonDF = amazonDF[amazonDF.Betrag.notnull()]
amazonDF = amazonDF.drop(['Kartennummer','Fremd','Kurs'],axis = 1)
amazonDF = amazonDF[~amazonDF['Umsatz'].str.contains("ZAHLUNG-LASTSCHRIFT")]
amazonDF['Betrag'] = amazonDF['Betrag'].str.replace('.','')
amazonDF['Betrag'] = amazonDF['Betrag'].str.replace(',','.')

giroDF = pd.read_csv(giroPath, sep=';')
giroDF = giroDF.drop(['Vorgang'],axis=1)
giroDF = giroDF.dropna(axis = 1, how = "all")
giroDF.columns = ['Buchungsdatum','Kaufdatum','Umsatz','Betrag']
giroDF = giroDF[~giroDF['Umsatz'].str.contains("Visa-Monatsabrechnung|Landesbank Berlin")]
giroDF['Betrag'] = giroDF['Betrag'].str.replace('.','')
giroDF['Betrag'] = giroDF['Betrag'].str.replace(',','.')

visaDF = pd.read_csv(visaPath, sep=';')
visaDF = visaDF.drop(['Vorgang','Referenz'],axis=1)
visaDF = visaDF.dropna(axis = 1, how = "all")
visaDF.columns = ['Buchungsdatum','Kaufdatum','Umsatz','Betrag']
visaDF = visaDF[~visaDF['Umsatz'].str.contains("WECHSELGELD-SPARBETRAG|MONATSABRECHNUNG")]
visaDF['Betrag'] = visaDF['Betrag'].str.replace('.','')
visaDF['Betrag'] = visaDF['Betrag'].str.replace(',','.')

result = amazonDF.append(giroDF)
result = result.append(visaDF)
result = result.reset_index()
result = result.drop('index', axis=1)
result.Umsatz = result['Umsatz'].str.lower()
result['Kategorie'] = 'Anders'

rulesPath = "./regeln.csv"
rulesDF = pd.read_csv(rulesPath, sep=";")

restResult = result.copy()
outputDF = pd.DataFrame()

for i in rulesDF.index:
    regexp = re.compile(rulesDF.loc[i,'Regeln'])
    partResult=restResult[restResult['Umsatz'].str.contains(regexp)]
    partResult.loc[:,'Kategorie'] = rulesDF.loc[i,'Kategorie']
    outputDF = outputDF.append(partResult)
    restResult = restResult[~restResult['Umsatz'].str.contains(regexp)]

outputDF = outputDF.append(restResult)
outputDF = outputDF.reset_index()
outputDF = outputDF.drop('index',axis=1)

outputPath = "./ergebnisse/ergebnis"+date+".csv"
outputDF.to_csv(outputPath,sep=';',index = False)
