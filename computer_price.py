# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:52:37 2021

@author: Hugo
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle 
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('xgboost_computer_price.pkl','rb'))
@app.route('/', methods=['GET'])

def Home():
    return render_template('home.html')

standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])

def predict():
    if request.method == 'POST':
        speed=int(request.form['speed'])
        hd=int(request.form['hd'])
        ram=int(request.form['ram'])
        screen=int(request.form['screen'])
        cd=request.form['cd']
        if(cd=='Yes'):
            cd = 1
        else:
            cd = 0
        multi=request.form['multi']
        if(multi=='Yes'):
            multi= 1
        else:
            multi= 0
        premium=request.form['premium']
        if(premium=='Yes'):
            premium= 1
        else:
            premium= 0
        ads=int(request.form['ads'])
        trend=int(request.form['trend'])
        prediction= model.predict(np.array([[speed, hd, ram,screen,cd,multi,premium,ads,trend]]))
        #prediction= model.predict([[speed, hd, ram,screen,cd,multi,premium,ads,trend]])
        pred = round(prediction[0],2)
        output=round(pred,2)
        
        
        if output <0:
            return render_template('home.html', prediction_text= "There is a mistake in the values introduced")
        else:
            return render_template('home.html', prediction_text= "A good price would be: {}".format(output))
    else:
        return render_template('home.html')
if __name__ == '__main__':
    app.run(debug= True)
