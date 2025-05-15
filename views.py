from django.shortcuts import render
from django.template import RequestContext
import pymysql
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
import os
import cv2
import numpy as np
from keras.utils.np_utils import to_categorical
from keras.layers import  MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D
from keras.models import Sequential
from keras.models import model_from_json
import datetime

global index
index = 0
global missing_child_classifier
global cascPath
global faceCascade

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def WelfareLogin(request):
    if request.method == 'GET':
       return render(request, 'WelfareLogin.html', {})

def WelfareLoginAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'welfare' and password == 'welfare':
            context= {'data':'welcome '+username}
            return render(request, 'WelfareScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'WelfareLogin.html', context)    

def ParentRegister(request):
    if request.method == 'GET':
       return render(request, 'ParentRegister.html', {})    

def Upload(request):
    if request.method == 'GET':
       return render(request, 'Upload.html', {})

def ParentLogin(request):
    if request.method == 'GET':
       return render(request, 'ParentLogin.html', {})

def ParentLoginAction(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      index = 0
      con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
      with con:    
          cur = con.cursor()
          cur.execute("select * FROM parentsignup")
          rows = cur.fetchall()
          for row in rows: 
             if row[0] == username and password == row[1]:
                index = 1
                break		
      if index == 1:
          file = open('session.txt','w')
          file.write(username)
          file.close()   
          context= {'data':'welcome '+username}
          return render(request, 'ParentScreen.html', context)
      else:
          context= {'data':'login failed'}
          return render(request, 'ParentLogin.html', context)

def ChildDetails(request):
    if request.method == 'GET':
       return render(request, 'ChildDetails.html', {})

def AdoptionRules(request):
    if request.method == 'GET':
       return render(request, 'AdoptionRules.html', {})    

def checkImage(name):
    index = 0
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select childname FROM adoption")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == name:
                index = 1
                break
    return index

def getDetails(name):
    parent = ''
    age = ''
    occupation = ''
    contact = ''
    email = ''
    address = ''
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM parentsignup")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == name:
                parent = row[2]
                age = row[3]
                occupation = row[4]
                contact = row[5]
                email = row[6]
                address = row[7]
                break
    return parent, age, occupation, contact, email, address

def ViewAdoption(request):
    if request.method == 'GET':
        output = '<table border=1 align=center>'
        output+='<tr><th>Parent Name</th><th>Parent age</th><th>Occupation</th><th>Contact No</th><th>Email ID</th><th>Address</th><th>Child Name</td></tr>'
        color = '<font size="" color="black">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
        with con:    
          cur = con.cursor()
          cur.execute("select * FROM adoption")
          rows = cur.fetchall()
          for row in rows:
              user = row[0]
              child = row[1]
              parent, age, occupation, contact, email, address = getDetails(user)
              output+='<tr><td>'+color+parent+'</td>'
              output+='<td>'+color+age+'</td>'
              output+='<td>'+color+occupation+'</td>'
              output+='<td>'+color+contact+'</td>'
              output+='<td>'+color+email+'</td>'
              output+='<td>'+color+address+'</td>'
              output+='<td>'+color+child+'</td></tr>'
        output+='</table><br/><br/><br/><br/><br/>'
        context= {'data':output}
        return render(request, 'ViewAdoption.html', context)      

def AdoptAction(request):
    if request.method == 'GET':
        name = request.GET.get('name', False)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO adoption(username,childname,adoption_date) VALUES('"+user+"','"+name+"','"+str(current_time)+"')"
        db_cursor.execute(query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        output = ''
        parent, age, occupation, contact, email, address = getDetails(user)
        output = '<table border=1 align=center>'
        output+='<tr><th>Parent Name</th><th>Parent age</th><th>Occupation</th><th>Contact No</th><th>Email ID</th><th>Address</th><th>Child Name</td></tr>'
        color = '<font size="" color="black">'
        output+='<tr><td>'+color+parent+'</td>'
        output+='<td>'+color+age+'</td>'
        output+='<td>'+color+occupation+'</td>'
        output+='<td>'+color+contact+'</td>'
        output+='<td>'+color+email+'</td>'
        output+='<td>'+color+address+'</td>'
        output+='<td>'+color+name+'</td></tr></table><br/><br/><br/><br/><br/>'
        context= {'data':output}
        return render(request, 'Certificate.html', context)

def ChildDetailsAction(request):
    if request.method == 'POST':
      age = request.POST.get('t1', False)
      colour = request.POST.get('t2', False)
      user = ''
      index = 0
      with open("session.txt", "r") as file:
          for line in file:
              user = line.strip('\n')
      file.close        
      con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
      with con:    
          cur = con.cursor()
          cur.execute("select child_age,child_color FROM parentsignup where username='"+user+"'")
          rows = cur.fetchall()
          for row in rows:
              if row[0] == age and row[1] == colour:
                  index = 1
      if index == 1:
          imgs = ['002A03.JPG','049A10.JPG','053A03.JPG','053A04.JPG','053A06.JPG']
          output = '<table border=1 align=center>'
          output+='<tr><th>Username</th><th>Child Image</th><th>Adopt Child</th></tr>'
          color = '<font size="" color="black">'
          for i in range(len(imgs)):
              if checkImage(imgs[i]) == 0:
                  output+='<tr><td>'+color+user+'</td><td><img src=/static/testImages/'+imgs[i]+' width=200 height=200></img></td>'
                  output+='<td><a href=\'AdoptAction?name='+imgs[i]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
          output+='</table><br/><br/><br/><br/>'        
          context= {'data':output}
          return render(request, 'ViewImages.html', context)
      else:
          context= {'data':"child details mismatch"}
          return render(request, 'ParentScreen.html', context)          

def OfficialLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'admin' and password == 'admin':
       context= {'data':'welcome '+username}
       return render(request, 'OfficialScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Login.html', context)

def ViewUpload(request):
    if request.method == 'GET':
       strdata = '<table border=1 align=center width=100%><tr><th>Upload Person Name</th><th>Child Name</th><th>Contact No</th><th>Found Location</th><th>Child Image <th>Uploaded Date</th><th>Status</th></tr><tr>'
       con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
       with con:
          cur = con.cursor()
          cur.execute("select * FROM missing")
          rows = cur.fetchall()
          for row in rows: 
             strdata+='<td>'+row[0]+'</td><td>'+str(row[1])+'</td><td>'+row[2]+'</td><td>'+row[3]+'</td><td><img src=/static/photo/'+row[4]+' width=200 height=200></img></td><td>'
             strdata+=str(row[5])+'</td><td>'+str(row[6])+'</td></tr>'
    context= {'data':strdata}
    return render(request, 'ViewUpload.html', context)
    


def UploadAction(request):
     global index
     global missing_child_classifier
     global cascPath
     global faceCascade
     if request.method == 'POST' and request.FILES['t5']:
        output = ''
        person_name = request.POST.get('t1', False)
        child_name = request.POST.get('t2', False)
        contact_no = request.POST.get('t3', False)
        location = request.POST.get('t4', False)
        myfile = request.FILES['t5']
        fs = FileSystemStorage()
        filename = fs.save('C:/Python/MissingChilds/MissingChildApp/static/photo/'+child_name+'.png', myfile)
        #if index == 0:
        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        #index = 1
        option = 0;
        frame = cv2.imread(filename)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,1.3,5)
        print("Found {0} faces!".format(len(faces)))
        img = ''
        status = 'Child not found in missing database'
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                img = frame[y:y + h, x:x + w]
                option = 1
        if option == 1:
            with open('model/model.json', "r") as json_file:
                loaded_model_json = json_file.read()
                missing_child_classifier = model_from_json(loaded_model_json)
            missing_child_classifier.load_weights("model/model_weights.h5")
            missing_child_classifier.make_predict_function()   
            img = cv2.resize(img, (64,64))
            im2arr = np.array(img)
            im2arr = im2arr.reshape(1,64,64,3)
            img = np.asarray(im2arr)
            img = img.astype('float32')
            img = img/255
            preds = missing_child_classifier.predict(img)
            if(np.amax(preds) > 0.60):
                status = 'Child found in missing database'
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        filename = os.path.basename(filename)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO missing(person_name,child_name,contact_no,location,image,upload_date,status) VALUES('"+person_name+"','"+child_name+"','"+contact_no+"','"+location+"','"+filename+"','"+str(current_time)+"','"+status+"')"
        db_cursor.execute(query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        context= {'data':'Thank you for uploading. '+status}
        return render(request, 'Upload.html', context)



def ParentRegisterAction(request):
    if request.method == 'POST' and request.FILES['t9']:
        output = ''
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        parent = request.POST.get('t3', False)
        age = request.POST.get('t4', False)
        occupation = request.POST.get('t5', False)
        contact = request.POST.get('t6', False)
        email = request.POST.get('t7', False)
        address = request.POST.get('t8', False)
        child_age = request.POST.get('t10', False)
        child_color = request.POST.get('t11', False)
        myfile = request.FILES['t9']
        filenames = request.FILES['t9'].name
        fs = FileSystemStorage()
        filename = fs.save('C:/Python/MissingChilds/MissingChildApp/static/documents/'+filenames, myfile)

        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'MissingChildDB',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO parentsignup(username,password,name,age,occupation,contactno,email,address,filename,child_age,child_color) VALUES('"+username+"','"+password+"','"+parent+"','"+age+"','"+occupation+"','"+contact+"','"+email+"','"+address+"','"+filenames+"','"+child_age+"','"+child_color+"')"
        db_cursor.execute(query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        context= {'data':'Signup process completed'}
        return render(request, 'ParentRegister.html', context)











    
        
