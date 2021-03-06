from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
from datetime import date
import os
from collections import Counter
from bson import json_util
import sqlite3
db = 'Database/db.sqlite3'
#SAMPLE DATABASE
conn = sqlite3.connect(db)
app = Flask(__name__)
app.secret_key= ''

cur = conn.cursor()

#INITIAL QUERIES GO HERE
cur.execute('''CREATE TABLE IF NOT EXISTS patients (id integer NOT NULL UNIQUE,
				name varchar(20) NOT NULL,
				gender varchar(20) NOT NULL,
				update_date date NOT NULL,
				state varchar(200),
				reason varchar(50) NOT NULL,
				age integer NOT NULL,
				PRIMARY KEY(id)	
				);''')
conn.commit()
conn.close()

#PRINTS ALL TABLES
def check_tables():		
	with sqlite3.connect(db) as conn:
		cur = conn.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
		var = cur.fetchall()
		print(var)

# For static files
@app.route('/static/<path:filename>')
def getFile(filename):
	return send_file("static/" + filename)

@app.route('/templates/<path:filename>')
def showTemplate(filename):
	return render_template(filename, data="You can add data here")

@app.route('/')
def index():
	return render_template('index.html',alert = False)

@app.route('/patient')
def patient_form():
    return render_template('patientform.html')

@app.route('/addpatient', methods = ['POST'])
def add_patient():
    if request.method == 'POST':
        pid = request.form['id']
        name = request.form['name']
        gender = request.form['gender']
        update_date = date.today()
        state = request.form['state']
        reason = request.form['reason']
        age = request.form['age']

        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO patients VALUES(?,?,?,?,?,?,?)",[pid,name,gender,update_date,state,reason,age])
            conn.commit()

    return render_template('index.html',alert = True)

@app.route('/report')
def report():
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients")
        patients = cur.fetchall()
        ages = {}
        reason = {}
        for i in range(len(patients)):
            if patients[i][6] in ages.keys():
                ages[patients[i][6]] += 1
            else:
                ages[patients[i][6]] = 1
            # ages.append(patients[i][6])
            if patients[i][5] in reason.keys():
                reason[patients[i][5]] += 1
            else:
                reason[patients[i][5]] = 1
        # reasonCount = Counter(reason)
        # print(ages)
        # print(reasonCount['hello'])
        # ageCounter = Counter(ages)
        
    return render_template('report.html',age=ages,reason = reason)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/api/search' , methods = ['POST'])
def search_name():
    response = {}
    
    data = request.get_json()
    name = data['name']
    patients = []
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients WHERE name like ?",('%'+name+'%',))
        patients = cur.fetchall()
    response = patients

    return json_util.dumps(response)


if __name__ == '__main__':
    app.run(port=5000,debug = True)