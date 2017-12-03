import sqlite3 as sql
from flask import Flask, request
from flask import render_template
from collections import OrderedDict

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', header='Demo for CS2300')

@app.route('/insert/<itype>')
def insert(itype):
    content = OrderedDict()
    if itype == 'part':
        content['a_date'] = 'Arrival Date'
        content['name'] = 'Name'
        content['part_id'] = 'Part ID'
        content['serial'] = 'Serial Number'
        content['price']='Price'
        content['mname'] =  'Manufacturer\'s Name'
        url='add_part'
    elif itype == 'man':
        content['name'] =  'Name'
        content['address'] =  'Address'
        url = 'add_man'
    elif itype == 'order':
        content['pay_info'] = 'Payment Information'
        content['order_ID'] = 'Order ID'
        content['date_ordered'] = 'Date Ordered'
        content['total_price'] = 'Total Price'
        url = 'add_order'
    elif itype == 'cust':
        content['fname'] = 'First Name'
        content['lname'] = 'Last Name'
        content['email']= 'Email'
        content['cust_id'] = 'Customer ID'
        content['number'] = 'Phone Number'
        content['stadd']= 'Street Address'
        content['zip']= 'Zip Code'
        content['state']= 'State'
        url = 'add_cust'
    elif itype == 'op':
        content['part_id']= 'Part ID'
        content['quantity']= 'Quantity'
        content['discount']= 'Discount'
        content['receipt_num']= 'Receipt Number'
        content['retail_price']= 'Retail Price'
        url = 'add_op'
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


@app.route('/addcust', methods=["POST", "GET"])
def add_cust():
    msg = ""
    if request.method == 'POST':
        try:
            fname = request.form["fname"]
            lname = request.form["lname"]
            email = request.form["email"]
            cust_id = request.form["cust_id"]
            number = request.form["number"]
            stadd = request.form["stadd"]
            _zip_ = request.form["zip"]
            state = request.form["state"]

            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO customer (fname, lname, email, cust_id, number, stadd, zip, state) VALUES (?,?,?,?,?,?,?,?)",(fname, lname, email, cust_id, number, stadd, _zip_, state))
                con.commit()
                msg = "Added customer successfully"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg = msg)
            con.close()


@app.route('/addorder', methods=["POST", "GET"])                                                                                                                                                                
def add_order():
    msg = ""                                                                                                                                                                                                       
    if request.method == 'POST':                                                                                                                                                                                   
        try:                                                                                                                                                                                                       
            pay_info = request.form["pay_info"] 
            total_price = request.form["total_price"]
            order_id = request.form["order_id"]
            date_ordered = request.form["date_ordered"]
                                                                                                                                                                                                                   
            with sql.connect("test3.db") as con:                                                                                                                                                                   
                cur = con.cursor()                                                                                                                                                                                 
                cur.execute("INSERT INTO order (pay_info, total_price, order_id, date_ordered) VALUES (?,?,?,?)",(pay_info, total_price, order_id, date_ordered)) 
                con.commit()                                                                                                                                                                                       
                msg = "Added order successfully"                                                                         
        except:                                                                                                                                                                                                    
            con.rollback()                                                                                                                                                                                         
            msg = "error in insert operation"                                                                                                                                                                      
                                                                                                                                                                                                                   
        finally:                                                                                                                                                                                                   
            return render_template("result.html", msg = msg)                                                                                                                                                       
            con.close()

@app.route('/addop', methods=["POST", "GET"])
def add_op():
    msg = ""
    if request.method == 'POST':
        try:
            part_id = request.form["part_id"]
            quantity = request.form["quantity"]
            discount = request.form["discount"]
            receipt_num = request.form["receipt_num"]
            retail_price = request.form["retail_price"]
            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO ordered_part (part_id, quantity, discount, receipt_num, retail_price) VALUES (?,?,?,?,?)",(part_id, quantity, discount, receipt_num, retail_price))
                con.commit()
                msg = "Added ordered part successfully"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg = msg)
            con.close()


@app.route('/list/<itype>')
@app.route('/list')
def list(itype='null'):
    if itype == 'null':
        con = sql.connect("test3.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM part")
        rows = cur.fetchall()
        names = [description[0] for description in cur.description]
        itype = 'part'
    elif itype == 'part' or itype == 'customer' or itype == 'manufacturer' or itype == 'order' or itype == 'ordered_part':
        con = sql.connect("test3.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        com = "SELECT * FROM " + itype
        cur.execute(com)
        names = [description[0] for description in cur.description]
        rows = cur.fetchall()
        print(type(rows[0]))
        print(names)
    else:
        return render_template('index.html')
    return render_template("list.html", rows = rows, names = names, tname=itype)


@app.route('/display/<itype>/<ident1>/<ident2>')
@app.route('/display/<itype>/<ident1>')
@app.route('/display')
def display(itype,ident1='Anon',ident2='Anon'):
    print(itype, ident1, ident2)
    if itype == 'Anon':
        return render_template('index.html')
    primk = {'part': 'part_id',
             'manufacturer': 'name',
             'customer': 'cust_id',
             'order': 'order_id'}

    con = sql.connect("test3.db")
    cur = con.cursor()
    if itype == 'op':
        com = 'SELECT * FROM ordered_part WHERE receipt_num=' + ident1 + ' AND order_id=' + ident2
        cur.execute(com)
        row = cur.fetchone()
        names = [description[0] for description in cur.description]
        return render_template('display.html', row = row, names = names)
    com = 'SELECT * FROM ' + itype + ' WHERE ' + primk[itype] + '= \'' + ident1 + '\''
    print(com)
    cur.execute(com)
    row = cur.fetchone()
    names = [description[0] for description in cur.description]
    return render_template('display.html', row=row, names=names)















