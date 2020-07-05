from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
from datetime import date
import os
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

if __name__ == '__main__':
    app.run(port=5000,debug = True)