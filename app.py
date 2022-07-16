from multiprocessing.sharedctypes import Value
import os
from time import time
from turtle import heading
from unicodedata import name
from uuid import uuid4
from flask import Flask, redirect, render_template, request,send_from_directory, url_for
##import tensorflow as tf
global graph,model
import json
from tkinter import *
##graph = tf.get_default_graph()
##import detection

headings = ("ID","Paitent Name","Gender","Paitent Age","Clinic Name","Clinic ID","Diagnosis","Date","Doctor"," ")

result = 0
global checkData
##ml = detection.detectp()
     
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
   return render_template("welcome.html")

@app.route("/")
def Complete():
   return render_template("complete.html")

@app.route('/index')
def Index():
    jsonFile = open("pneumoniadatacollection.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()
    return render_template('index.html',data=data)

@app.route('/edit/<id>',methods = ['POST','GET'])
def get_data(id):
    jsonFile = open("pneumoniadatacollection.json", "r+")
    data = json.load(jsonFile)
    
    for i in range(len(data)):
        if data[i]["ID"]==id:
            record = data[i]
    jsonFile.close()
    return render_template('edit.html',data= record)

@app.route('/update/<string:id>',methods=['POST'])
def update(id):
        paitentname = request.form.get('paitentname')
        gender      = request.form.get('gender')
        patientage  = request.form.get('patientage')
        clinicname  = request.form.get('clinicname')
        imageid     = request.form.get('imageid')
        type        = request.form.get('type')
        date        = request.form.get('date')
        doctorname  =request.form.get('doctorname')
        jsonFile = open("pneumoniadatacollection.json", "r+")
        data = json.load(jsonFile)
    
        for i in range(len(data)):
            if data[i]['ID']==id:
                data.pop(i)
                break
        entry={"ID":id,"paitentname":paitentname,"gender":gender,"patientage":patientage,"clinicname":clinicname,"imageid":imageid,"type":type,"date":date,"doctorname":doctorname}
        data.append(entry)
        with open('pneumoniadatacollection.json', 'w') as f:
            f.write(json.dumps(data, indent=9, separators=(',', ': ')))
        return redirect(url_for('Index'))
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete(id):
    obj = json.load(open("pneumoniadatacollection.json","r+"))
    for i in range(len(obj)):
        if obj[i]['ID']==id:
            obj.pop(i)
            break
    open("pneumoniadatacollection.json","w").write(
        json.dumps(obj,sort_keys=True,indent=4,separators=(',',':'))
    )
    return redirect(url_for('index'))


# @app.route("/upload",methods=["GET","POST"])
# def upload():
#    form = uploadform()
#    if form.is_submitted():
#        result= request.form
#        return render_template('user.html',result=result)
#    return render_template('upload.html',form=form)
@app.route("/form")
def form():
    return render_template('upload.html')

@app.route("/upload", methods=["POST"])
def upload():
    paitentname = request.form.get("paitentname")
    gender = request.form.get("gender")
    paitentage = request.form.get("paitentage")
    clinicname=request.form.get("clinicname")
    imageid= request.form.get("imageid")
    type=request.form.get("type")
    date=request.form.get("date")
    doctorname=request.form.get("doctorname")
    
    
    # Image folder 
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    targetReport = os.path.join(APP_ROOT,'report/')
    
    targetRep = os.path.join(APP_ROOT,'doctoroffice/')

    if not os.path.isdir(target):
            os.mkdir(target)
    if not os.path.isdir(targetReport):
            os.mkdir(targetReport)
    if not os.path.isdir(targetRep):
            os.mkdir(targetRep)
    for upload in request.files.getlist("file"):
        file_name = str(uuid4())
        print(file_name)
        destination = "/".join([target, f'{file_name}.jpg,.dcm'])
        upload.save(destination)
    for uploadReport in request.files.getlist("file1"):
        destinationReport = "/".join([targetReport, f'{file_name}.jpg'])
        uploadReport.save(destinationReport)
    for uploadRep in request.files.getlist("fil"):
        destinationRep = "/".join([targetRep, f'{file_name}.jpg'])
        uploadRep.save(destinationRep)
    
    jsonfilename='pneumoniadatacollection.json'


    if os.path.getsize(jsonfilename) == 0:
        entryFirst = [{"ID":file_name,"paitentname":paitentname,"gender":gender,"patientage":paitentage,"clinicname":clinicname,"imageid":imageid,"type":type,"date":date,"doctorname":doctorname}]
        with open(jsonfilename,mode='w') as f:
            json.dump(entryFirst,f)
    else:
        with open(jsonfilename, "r+") as file:
            data = json.load(file)
            entry={"ID":file_name,"paitentname":paitentname,"gender":gender,"patientage":paitentage,"clinicname":clinicname,"imageid":imageid,"type":type,"date":date,"doctorname":doctorname}
        for element in data:
            if(element['paitentname'] == entry['paitentname'] and element['imageid'] == entry['imageid']):
                checkData = "Not Found"
                break
            else:
                checkData = "Found"
                
        if checkData == "Found":
            print("Okay Working")
            data.append(entry)
            with open(jsonfilename,'w') as file:
                json.dump(data,file)
            

    return render_template('upload.html')


    
    #return render_template("complete.html",result=round(result*100,3))
@app.route("/detection")
def detection():
    return render_template('detection.html')
@app.route("/detectResult")
def detectResult():
    return render_template('complete.html')

@app.route("/confirm",methods=['GET','POST'])
def search():
    obj = json.load(open("pneumoniadatacollection.json","r+"))
    #if request.method == "POST":
    imageid = request.form.get("imageid")
    for i in range(len(obj)):
        if obj[i]['imageid']==imageid:
            record=obj[i]
            print(record['ID'])
            return render_template(url_for('confirm'),data=record)
    return render_template("search.html")
@app.route("/DoctorDiagnosis/<string:imageid>")
def confirm(imageid):
    return redirect(url_for('searchID'))
@app.route("/search")
def searchID():
    return render_template('search.html')

@app .route("/upload")
def send_image():
    return send_from_directory("images", "heatmap.png")

if __name__ == "__main__":
    app.run(port=80)