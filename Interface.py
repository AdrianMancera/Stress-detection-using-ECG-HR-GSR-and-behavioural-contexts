from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from keras.models import load_model

app = Flask(__name__)
 
@app.route('/')
def home():
    return render_template("input.html")

@app.route('/predict', methods=['POST' ,'GET'])
def result():
    l=['Lying  down', 'Sleeping','With friends', 'Shopping', 'Running', 'Excersise', 'At gym','At party', 'Bicycling', 'At main workplace', 'Watching TV','Surfing the Internet', 'Computer Work', 'Phone In Hand','In a meeting', 'Lab work', 'In class', 'Drinking(Alcohol)']
    s=[]
    for i in l:
        s.append(i)
    t=[]
    for i in range(1,19):
        #print("enter the avg time you spend "+l[i-1]+" in a week")
        t.append(float(request.form[str("v"+str(i))]))
    for i in range(17):
        for j in range(17-i):
            if(t[j+1]>t[j]):
                t[j+1],t[j]=t[j],t[j+1]
                s[j+1],s[j]=s[j],s[j+1]
    t5=s[:5]
    f=[]
    for i in l:
        if(i in t5):
            f.append(1)
        else:
            f.append(0)

    final=[float(request.form["ECG"]),float(request.form["HR"]),float(request.form["Hand_GSR"]),float(request.form["Foot_GSR"])]
    final.extend(f)
   #print("Final",final)
    if(int(request.form["choice"])==1):
        savedModelr=load_model('RegressionModel.h5')
        p=savedModelr.predict(np.array([final]))[0][0]
        if(p>1):
             p=1
        if(p<0):
            p=0
        return(render_template("result.html",msg="Your stress level is "+str(p)))
    if(int(request.form["choice"])==0):
        savedModelc=load_model('ClassificationModel.h5')
        p=savedModelc.predict_classes(np.array([final]))[0][0]
        if(p==1):
            return(render_template("result.html",msg="You are stressed!!!"))
        else:
            return(render_template("result.html",msg="You are not stressed!!"))

    
if __name__ == '__main__':
    app.run()