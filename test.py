#Testing model accuracy
from sklearn import linear_model
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import math
import pandas
df = pandas.read_csv("AQI.csv")
Y_val=[]
x_val=[]
x0=0
x1=0
x2=0
x3=0
x4=0
x5=0
X0=0
X1=0
X2=0
X3=0
X4=0
X5=0
for i in range(1000):
    X = df[['Avg1','Avg2','Avg3','Avg5']].values
    #print(X)
    y1 = df['AQI']
    X_train, X_test, y_train, y_test = train_test_split(X, y1, test_size=0.2) 
    #print(y)
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    X=0
    x=0
    for y in range(len(X_test)-1):
        i=regr.predict([X_test[y]])
        if i<50:
            if(y_test.values[y]<50):
                X=X+1
                X0=X0+1
            x0=x0+1
        elif i<101:
            if(y_test.values[y]<101):
                X=X+1
                X1=X1+1
            x1=x1+1
        elif i<150:
            if(y_test.values[y]<150):
                X=X+1
                X2=X2+1
            x2=x2+1
        if i<200:
            if(y_test.values[y]<200):
                X=X+1
                X3=X3+1
            x3=x3+1
        elif i<300:
            if(y_test.values[y]<300):
                X=X+1
                X4=X4+1
            x4=x4+1
        else:
            X=X+1
            X5=X5+1
            x5=x5+1
    x=len(X_test)
    Y_val.append(X/x)
    x_val.append(i)
import matplotlib.pyplot as plt
y=[X3/x3,X4/x4,X5/x5]
x=['Level 4', 'Level 5', 'Toxic']
plt.bar(x, y)
print(sum(Y_val)/len(Y_val))
