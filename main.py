#Importing required libraries
import json
from urllib.request import urlopen
import requests
from sklearn import linear_model
from sklearn.metrics import r2_score
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from sklearn.model_selection import train_test_split
import math
import pandas

industry_coords=[['A',34,-84],['A1',0,0],['A-1',34,-84]]
industry_coords_copy=industry_coords
a=[]
a0=[]

#Data from web-scraping starts

#Finding wind speeds for last day for tracking pollutants
page = requests.get('https://weather.com/en-IN/weather/hourbyhour/l/cc76c08b470b5ddd6e64efd9ce8f256542cfed4ba52f6c00a30a74da519cd070')
soup = BeautifulSoup(page.content, 'html.parser')
blog=soup.findAll('span',attrs={"class":"Wind--windWrapper--3Ly7c undefined"})

for title in blog:
    k=title.text
    a.append(k.split(' ')[0])
    a0.append(float(k.split(' ')[1]))
    print(k)

#Finding Humidity
page = requests.get('https://weather.com/en-IN/weather/today/l/cc76c08b470b5ddd6e64efd9ce8f256542cfed4ba52f6c00a30a74da519cd070')
soup = BeautifulSoup(page.content, 'html.parser')
blog=soup.findAll('span',attrs={"data-testid":"PercentageValue"})
for title in blog:
    k=title.text
avg3=float(k.replace("%",""))   
print(avg3)

#Finding Dew Point
blog=soup.findAll('span',attrs={"data-testid":"TemperatureValue"})
i=0
for title in blog:
    k=title.text
    if(i>=10):
        break
    i=i+1
avg2=float(k.replace("°",""))

#Finding avg. temp
blog=soup.findAll('span',attrs={"data-testid":"TemperatureValue"})
i=0
avg1=0
for title in blog:
    k=title.text
    if(i==1 or i==2):
        avg1=avg1+float(k.replace("°",""))
    i=i+1
avg1=avg1/2

#Finding Pressure
blog=soup.findAll('span',attrs={"data-testid":"PressureValue"})
i=0
for title in blog:
    k=title.text
avg5=float(k.replace(" mb","").replace("Arrow Up","").replace("Arrow Down",""))
print(avg5)

#Creating model and extracting AQI and weather training data
x2=a0
y2=[]
df = pandas.read_csv("AQI.csv")
x0=json.load(urlopen("https://ipinfo.io/"))['loc'].split(',')
# find all table with class-"twc-table"
x1=float(x0[0])
y=float(x0[1])
X = df[['Avg1', 'Avg2','Avg3','Avg5']].values
#print(X)
y1 = df['AQI']
#print(y)
regr = linear_model.LinearRegression()
regr.fit(X,y1)
x=regr.predict([[9/5*avg1+32,9/5*avg2+32,avg3,avg5*0.02953]])

#Printing predicted AQI
if x<50:
    print('Good')
elif x<101:
    print('Moderte')
elif x<150:
    print("Unhealthy for Sensitive People")
elif x<200:
    print("Unhealthy")
elif x<300:
    print("Hazardous")
else:
    print("Very Hazardous")
 
#Converting past wind to vectors to track pollutants
for i in a:
    if i=='N':
        y2.append(0)
    elif i=='NW':
        y2.append(-45)
    elif i=='WNW':
        y2.append(-67.5)
    elif i=='NNW':
        y2.append(-22.5)
    elif i=='NE':
        y2.append(45)
    elif i=='ENE':
        y2.append(67.5)
    elif i=='NNE':
        y2.append(22.5)
    elif i=='S':
        y2.append(180)
    elif i=='SW':
        y2.append(225)
    elif i=='WSW':
        y2.append(237.5)
    elif i=='SSW':
        y2.append(202.5)
    elif i=='SE':
        y2.append(135)
    elif i=='ESE':
        y2.append(112.5)
    elif i=='SSE':
        y2.append(157.5)
    elif i=='W':
        y2.append(-90)
    elif i=="E":
        y2.append(90)
#Converting
for i in range(len(y2)):
    y2[i]=y2[i]*math.pi/180
for i in range(len(x2)):
    x1=x1-(y2[i]*math.cos(x2[i]))*1/54.6
    y=y-(y2[i]*math.sin(x2[i]))*1/54.6
    
#Finding distance from pollution center
A1=[]
for i in industry_coords:
    A1.append((((i[1]-x1)**2+(i[2]-y)**2)**(1/2))*1/54.6)
A2=A1
A2.sort()

#Finding current AQI and comparing to forecasted API
blog=soup.findAll('text',attrs={"data-testid":"DonutChartValue"})
i=0
for title in blog:
    k=title.text
    if(i>=1):
        break
    i=i+1
AQI=float(k)
print(AQI)
print(x[0])

#Printing possible sources from our calculated coordinates and deciding penalty by comparing AQI
if((AQI-x[0])>50):
    print("Pollution coordinates:")
    print("%.4f"%x1)
    print("%.4f"%y)
    print("Most probable pollution sources in descending order of possibility:")
    for i in A2:
        print(industry_coords_copy[A1.index(i)][0])
        A1[A1.index(i)]=0
    print("Penalty as percentage of revenue:")
    print((AQI-x[0])/x[0]*100)
else:
    print("No penalty required")
