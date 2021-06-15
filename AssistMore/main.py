from flask import Flask,render_template,redirect,session,url_for,request,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import products
import orders
import uom
import orderdelete
import json
from sql_connection import get_sql_connection

app=Flask(__name__)
app.secret_key="1969"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="kilroy"
app.config["MYSQL_DB"]="assistmore"
		
db=MySQL(app)

connection=get_sql_connection()

@app.route('/')
def index():
    return render_template("assistmore.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        if 'email' in request.form and 'password' in request.form :
            email=request.form['email']
            password=request.form['password']
            cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM user_info WHERE email=%s AND password=%s",(email,password))
            info=cursor.fetchone()
            if info['email']==email and info['password']==password:
                return render_template("index.html")
            else:
                return render_template("login.html")
    return render_template("login.html")

@app.route('/newstaffloginverify', methods=['GET','POST'])
def newstaffloginverify():
        if request.method =='POST':
            if request.form['email'] == 'admin@123' and request.form['password'] == 'admin':
                return redirect(url_for('staffregister'))
        else:
            return redirect(url_for('newstaffverify'))

@app.route('/stafflogin', methods=['GET','POST'])
def stafflogin():
    if request.method=='POST':
        if 'email' in request.form and 'password' in request.form :
            email=request.form['email']
            password=request.form['password']
            cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM staff_info WHERE email=%s AND password=%s",(email,password))
            info=cursor.fetchone()
            if info['email']==email and info['password']==password:
                return render_template("index.html")
            return render_template("stafflogin.html")
    return render_template("stafflogin.html")


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['password2']
        cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO user_info(firstname,lastname,email,password,confirm_password)VALUES(%s,%s,%s,%s,%s)",(firstname,lastname,email,password,confirm_password))
        db.connection.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/staffregister', methods=['GET','POST'])
def staffregister():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['password2']
        cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO staff_info(firstname,lastname,email,password,confirm_password)VALUES(%s,%s,%s,%s,%s)",(firstname,lastname,email,password,confirm_password))
        db.connection.commit()
        return redirect(url_for('stafflogin'))
    return render_template("newstaffregister.html")

@app.route('/assistmore')
def assistmore():
    return render_template("assistmore.html")

@app.route('/newstaffverify')
def newstaffverify():
    return render_template("newstaffverify.html")
    

@app.route('/product')
def product():
    return render_template("manage-product.html")

@app.route('/dashboard')
def dashboard():
    return render_template("index.html")

@app.route('/order')
def order():
    return render_template("order.html")


@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteOrder', methods=['POST'])
def delete_order():
    return_id = orders.delete_order(connection,request.form['order_id'])
    response = jsonify({
        'order_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__=='__main__':
    app.run(debug=True)