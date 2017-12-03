import sqlite3 as sql
from flask import Flask, request
from flask import render_template
from datetime import datetime, timedelta


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', header='Demo for CS2300')

@app.route('/insert/<itype>')
def insert(itype):
    if itype == 'part':
        content = {'a_date':'Arrival Date',
                   'name':'Name',
                   'part_id':'Part ID',
                   'serial':'Serial Number',
                   'price':'Price',
                   'mname': 'Manufacturer\'s Name'}
        url='add_part'
    elif itype == 'man':
        content = {'name': 'Name',
                   'address': 'Address'}
        url = 'add_man'
    return render_template('insert.html', content=content, url=url)


@app.route('/addpart', methods=["POST", "GET"])
def add_part():
    msg = ""
    if request.method == 'POST':
        try:
            a_date = (request.form["a_date"])
            name = request.form["name"]
            part_id = int(request.form["part_id"])
            serial = int(request.form["serial"])
            price = float(request.form["price"])
            mname = request.form["mname"]

            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO part (a_date,name,part_id,serial,price) VALUES (?,?,?,?,?)",(a_date,name,part_id,serial,price))
                cur.execute("INSERT INTO made (name, part_id) VALUES (?,?)", (mname, part_id))
                con.commit()
                print("PLLLLLLLLLLLLLLEEEEEEEEEEEEAAAAAAAAAAASSSSSSSSSSEEEEEEEEEEE")
                msg = "Added part successfully"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg = msg)
            con.close()

@app.route('/addman', methods=["POST", "GET"])
def add_man():
    msg = ""
    if request.method == 'POST':
        try:
            name = request.form["name"]
            address = request.form["address"]

            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO manufacturer (name, address) VALUES (?,?)",(name, address))
                con.commit()
                msg = "Added manufacturer successfully"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg = msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("test3.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM part")

    rows = cur.fetchall()
    return render_template("list.html", rows = rows)


