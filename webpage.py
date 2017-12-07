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
    rows = ""
    content = OrderedDict()
    # content is an ordered dict so that when the elements are put into the webpage
    # their order is consistent.
    if itype == 'part':
        content['a_date'] = 'Arrival Date'
        content['name'] = 'Name'
        content['part_id'] = 'Part ID'
        content['serial'] = 'Serial Number'
        content['price']='Price'
        content['mname'] =  'Manufacturer\'s Name'
        # We populate a dropdown with manufacturers so we have to SELECT them for the database
        with sql.connect("test3.db") as con:
            cur = con.cursor()
            con.row_factory = sql.Row
            cur.execute("SELECT * FROM manufacturer")
            rows = cur.fetchall()
        url='add_part'
    elif itype == 'man':
        content['name'] =  'Name'
        content['address'] =  'Address'
        url = 'add_man'
    elif itype == 'order':
        content['order_id'] = 'Order ID'
        content['pay_info'] = 'Payment Information'
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
        content['order_id']= 'Order ID'
        content['quantity']= 'Quantity'
        content['discount']= 'Discount'
        content['retail_price']= 'Retail Price'
        url = 'add_op'
    return render_template('insert.html', content=content, url=url, rows=rows)


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
            vals = ("part_id", part_id)
            check = enforce("part", vals)
            # Checking to see if there is already an entity with the same primary key
            if check["error"]:
                return render_template('index.html',msg=check["msg"])

            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO part (a_date,name,part_id,serial,price) VALUES (?,?,?,?,?)",(a_date,name,part_id,serial,price))
                con.commit()
        except:
            con.rollback()
        finally:
            return render_template("index.html", msg = check["msg"])
            con.close()

@app.route('/addman', methods=["POST", "GET"])
def add_man():
    msg = ""
    if request.method == 'POST':
        try:
            name = request.form["name"]
            address = request.form["address"]
            # Checking that a manufacturer with the same name does not exist already
            check = enforce("manufacturer", ("name", name))
            if check["error"]:
                return render_template("index.html", msg=check["msg"])

            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO manufacturer (name, address) VALUES (?,?)",(name, address))
                con.commit()
        except:
            con.rollback()

        finally:
            return render_template("index.html", msg = check["msg"])
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
            check = enforce("customer", ("cust_id", cust_id))
            if check["error"]:
                return render_template("index.html", msg=check["msg"])

            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO customer (fname, lname, email, cust_id, number, stadd, zip, state) VALUES (?,?,?,?,?,?,?,?)",(fname, lname, email, cust_id, number, stadd, _zip_, state))
                con.commit()
        except:
            con.rollback()

        finally:
            return render_template("index.html", msg = check["msg"])
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
            check = enforce("order", ("order_id", order_id))
            if check["error"]:
                return render_template("index.html", msg=check["msg"])

            with sql.connect("test3.db") as con:                                                                                                                                                                   
                cur = con.cursor()                                                                                                                                                                                 
                cur.execute("INSERT INTO 'order' (order_id, pay_info, total_price, date_ordered) VALUES (?,?,?,?)",(order_id, pay_info, total_price, date_ordered)) 
                con.commit() 
        except:  
            con.rollback() 
        finally: 
            return render_template("index.html", msg = check["msg"]) 
            con.close()

@app.route('/addop', methods=["POST", "GET"])
def add_op():
    msg = ""
    if request.method == 'POST':
        try:
            part_id = request.form["part_id"]
            quantity = request.form["quantity"]
            discount = request.form["discount"]
            order_id = request.form["order_id"]
            retail_price = request.form["retail_price"]
            vals = (part_id, order_id)
            check = enforce("ordered_part", vals)
            if check["error"]:
                return render_template("index.html", msg=check["msg"])

            with sql.connect("test3.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO ordered_part (part_id, order_id, quantity, discount, retail_price) VALUES (?,?,?,?,?)",(part_id, order_id, quantity, discount, retail_price))
                con.commit()
        except:
            con.rollback()

        finally:
            return render_template("index.html", msg = check["msg"])
            con.close()


@app.route('/list/<itype>')
@app.route('/list')
def list(itype='null'):
    if itype == 'null':
        # accounting for manually putting in url
        return render_template('index.html')
    elif itype == 'part' or itype == 'customer' or itype == 'manufacturer' or itype == 'order' or itype == 'ordered_part':
        con = sql.connect("test3.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        # select all rows from the itype given
        com = "SELECT * FROM '" + itype + "'"
        cur.execute(com)
        # get all of the column names
        names = [description[0] for description in cur.description]
        # rows is all of the rows returned from the select statement
        rows = cur.fetchall()
    else:
        return render_template('index.html')
    return render_template("list.html", names=names, rows=rows, tname=itype)


@app.route('/display/<itype>/<ident1>/<ident2>')
@app.route('/display/<itype>/<ident1>')
@app.route('/display')
def display(itype,ident1='Anon',ident2='Anon'):
    if itype == 'Anon':
        return render_template('index.html', msg="Enter a type to see a list")
    # dict for all entries and their primary key as reference for commands
    primk = {'part': 'part_id',
             'manufacturer': 'name',
             'customer': 'cust_id',
             'order': 'order_id'}

    con = sql.connect("test3.db")
    cur = con.cursor()
    # accounting for ordered part having two primary keys
    if itype == 'ordered_part':
        com = 'SELECT * FROM ordered_part WHERE part_id=' + ident1 + ' AND order_id=' + ident2
        cur.execute(com)
        row = cur.fetchone()
        names = [description[0] for description in cur.description]
        tname = itype
        return render_template('display.html', row = row, names = names, tname=tname)
    cur.execute("SELECT * FROM '{}' WHERE {}=?".format(itype, primk[itype]), (ident1,))
    row = cur.fetchone()
    names = [description[0] for description in cur.description]
    tname = itype
    return render_template('display.html', row=row, names=names, tname=tname)


@app.route('/delete/<itype>/<ident>/<ident2>', methods = ["GET","POST"])
@app.route('/delete/<itype>/<ident>', methods=["GET","POST"])
def delete(itype, ident, ident2=None):
    try:
        with sql.connect("test3.db") as con:
            cur = con.cursor()
            # sqlite does not like having variables in delete statements so we have a case for each table
            if itype == "part":
                cur.execute("DELETE FROM part WHERE part_id = ?", (ident,))
            elif itype == "manufacturer":
                cur.execute("DELETE FROM manufacturer WHERE name = ?", (ident,))
            elif itype == "order":
                cur.execute("DELETE FROM 'order' WHERE order_id = ?", (ident,))
            elif itype == "customer":
                cur.execute("DELETE FROM customer WHERE cust_ID = ?", (ident,))
            elif itype == "ordered_part":
                cur.execute("DELETE FROM ordered_part WHERE part_id = ? AND order_id = ?", (ident, ident2))

            con.commit()
            msg = "Deleted successfully"

    except:
        msg="something went wrong with the deletion"
        con.rollback()
    finally:
        return render_template("index.html", msg=msg)

@app.route('/search/<itype>', methods=["GET","POST"])
def search(itype):
    if request.method == "POST":
        with sql.connect("test3.db") as con:
            cur = con.cursor()
            con.row_factory = sql.Row
            com = "SELECT * FROM '" + itype  + "' WHERE " + request.form["selection"] + "='" + request.form["search"] + "'"
            cur.execute(com)
            rows = cur.fetchall()
            names = [description[0] for description in cur.description]
            return render_template("list.html", rows=rows, names=names, tname=itype)

@app.route('/modify/<itype>', methods=["GET","POST"])
def modify(itype):
    if request.method == "POST":
        with sql.connect("test3.db") as con:
            cur = con.cursor()
            # for each possibility, we update the table with the values given to us by the user
            # we do this by putting all of the non-pk columns into a list and looping over an update statement
            if itype == "ordered_part":
                cols = ["quantity", "discount", "retail_price"]
                vals = [request.form["part_id"], request.form["order_id"]]
                for i in cols:
                    cur.execute("UPDATE '{}' SET {}={} WHERE part_id=? AND order_id=?".format(itype, i, request.form[i]), (vals[0], vals[1]))
                return render_template("index.html", msg="Successfully changed part!")
            elif itype == "part":
                cols = ["a_date", "name", "serial", "price"]
                vals = ["part_id", request.form["part_id"]]
                for i in cols:
                    cur.execute("UPDATE part SET {}=? WHERE part_id=?".format(i), (request.form[i], vals[1]))
                return render_template("index.html", msg="Successfully changed part!")
             
            elif itype == "manufacturer":
                cols = ["address"]
                vals = ["name", request.form["name"]]
                for i in cols:
                    cur.execute("UPDATE manufacturer SET {}=? WHERE name=?".format(i), (request.form[i], vals[1]))
                return render_template("index.html", msg="Successfully changed manufacturer!")
          
            elif itype == "order":
                cols = ["pay_info", "total_price", "date_ordered"]
                for i in cols:
                    cur.execute("UPDATE 'order' SET {}=? WHERE order_id=?".format(i), (request.form[i], request.form["order_id"]))
                return render_template("index.html", msg="Successfully changed order!")          

            elif itype == "customer":
                cols = ["fname", "lname", "email", "number", "stadd", "zip", "state"]
                vals = ["cust_id", request.form["cust_id"]]
                for i in cols:
                    cur.execute("UPDATE customer SET {}=? WHERE cust_id=?".format(i), (request.form[i], vals[1]))
                return render_template("index.html", msg="Successfully changed customer!")


def enforce(itype, vals):
    with sql.connect("test3.db") as con:
        cur = con.cursor()
        # have to account for two pk's in ordered_part
        if itype == 'ordered_part':
            cur.execute('SELECT * FROM ordered_part WHERE part_id=? AND order_id=?', (vals[0], vals[1]))
            if cur.fetchone():
                return {"msg": "Invalid: ordered_part with part_id={} and order_id={} already exists!".format(vals[0], vals[1]), 
                        "error": True}
            else:
                return {"msg": "Successfully completed action.",
                        "error": False}
        else:
            cur.execute("SELECT * FROM '{}' WHERE {}=?".format(itype, vals[0]), (vals[1],))
            if cur.fetchone() is not None:
                return {'msg': 'Invalid: {}={} already exists!'.format(vals[0], vals[1]),
                        'error': True}
            else:
                return {'msg': 'Successfully completed action.',
                        'error': False}
