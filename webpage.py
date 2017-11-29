import sqlite3
from flask import Flask, request
from flask import render_template

connection = sqlite3.connect('test.db;')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', header='Demo for CS2300')

@app.route('/submit', methods=["POST"])
def insert():
    field = request.form['form-field']
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO Stuff VALUES (:val)',
        {'val': field}
    )
    connection.commit()
    db_contents = cursor.execute(
        'SELECT * FROM Stuff'
    ).fetchall()
    return render_template('index.html', header='New Stuff', list_of_stuff=db_contents)

