# -*- coding: utf-8 -*-
import json
import pandas as pd
f = open('../assets/json/countries_data.json')
data = json.load(f)
dataAll = []

def getData(dataType):
    listHead = []
    listHead.append('国家或地区')
    for i in range(len(data[0]['list'])):
      listHead.append(data[0]['list'][i]['date'])

    dateList = [[] for i in range(len(data)+1)]
    dateList[0] = listHead
    for i in range(len(data)):
      dateList[i+1].append(data[i]['country'])
      for k in range(len(listHead)-1):
        dateList[i+1].append(str(data[i]['list'][k][dataType]))

    return dateList

dataAll.append(getData("total_confirm"))
dataAll.append(getData("total_death"))
dataAll.append(getData("total_cure"))

strList = list(str(dataAll))
for i in range(len(strList)-2):
  if ((strList[i] == '\'') & ((strList[i+1] != 'I') | (strList[i+2] != 'v'))):
      strList[i] = '\"'
strList = ''.join(strList)
print(strList)


file = open('../assets/json/cabarData.json','w',encoding='utf-8')
file.write(strList)
file.close()


