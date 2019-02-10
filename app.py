import datetime
import time
from flask import *
from flask_sqlalchemy import *
from passlib.hash import sha256_crypt
from config import *
from models.Orders import Orders
from models.Products import Products
from models.User import User
from models.Vendor import Vendor



######### User #########


@app.route('/')
def homepage():
    # if session['logged_in'] == False:
    return render_template("index.html")
    # else:
    #     if session['type'] == 'user':
    #         return redirect(url_for('user', uid=))


@app.route('/userlogin', methods=['POST','GET'])
def userlogin():	
    if request.method == "GET":
        return render_template("userlogin.html")
    else:
        RollNumber = request.form['rollnumber']
        password = request.form['password']
        user = User.query.filter_by(RollNumber=RollNumber).first()
        if not(user):
            flash("This RollNumber doesn't exists!")
            return redirect(url_for('userlogin'))
        else:
            password_correct = sha256_crypt.verify(password, user.Password)
            if not(password_correct):
                flash("Wrong password entered!")
                return redirect(url_for('userlogin'))
            else:
                flash("Logged in successfully:)")
                session['RollNumber'] = RollNumber
                session['UserId'] = user.UserId
                session['logged_in'] = True
                session['type'] = 'user'
        return redirect(url_for('userprofile',uid = session['UserId']))

@app.route('/userlogout/')
def userlogout():
    session.pop('RollNumber', None)
    session.pop('UserId', None)
    session.pop('logged_in', False)
    return redirect(url_for('homepage'))

@app.route('/userregister/', methods=['POST','GET'])
def userregister():
    if request.method == "GET":
        return render_template("userregister.html")
    else:
        rollnumber = request.form['rollnumber']
        password = request.form['password']
        hashed_password = sha256_crypt.hash(password)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone_no = request.form['phone_no']
        if len(phone_no)<10 or len(phone_no)>10:
            flash("Invalid Phone no!")
            return redirect(url_for('userregister'))
        for ch in phone_no:
            if not ch.isdigit():
                flash("Invalid Phone no!")
                return redirect(url_for('userregister'))
        user = User(RollNumber = rollnumber,
                    Password = hashed_password,
                    PhoneNumber = phone_no,
                    FirstName = firstname,
                    LastName = lastname)
        db.session.add(user)
        db.session.commit()
        db.session.close()
        flash("Successfully registered!")
        return redirect(url_for('userlogin'))


@app.route('/user/<int:uid>')
def userprofile(uid):
    vendors = Vendor.query.filter_by().all()
    if 'UserId' in session and session['UserId'] == uid:
        user = User.query.filter_by(UserId = uid).first_or_404()
        orders = Orders.query.filter_by(UserId = uid).all()
        products = Products.query.all()
        return render_template("userProfile.html", user = user, orders = orders, products = products, vendors = vendors)



######### Vendor ############




@app.route('/venlogin', methods=['POST','GET'])
def venlogin(): 
    if request.method == "GET":
        return render_template("venlogin.html")
    else:
        Title = request.form['title']
        password = request.form['password']
        vendor = Vendor.query.filter_by(Title=Title).first()
        if not(vendor):
            flash("This Title doesn't exists!")
            return redirect(url_for('venlogin'))
        else:
            password_correct = sha256_crypt.verify(password, vendor.Password)
            if not(password_correct):
                flash("Wrong password entered!")
                return redirect(url_for('venlogin'))
            else:
                flash("Logged in successfully:)")
                session['Title'] = Title
                session['VendorId'] = vendor.VendorId
                session['logged_in'] = True
                session['type'] = 'vendor'
        return redirect(url_for("venprofile", VendorId = session['VendorId']))

@app.route('/venlogout/')
def venlogout():
    session.pop('Title', None)
    session.pop('VendorId', None)
    session.pop('logged_in', False)
    return redirect(url_for('homepage'))

@app.route('/venregister/', methods=['POST','GET'])
def venregister():
    if request.method == "GET":
        return render_template("venregister.html")
    else:
        title = request.form['title']
        password = request.form['password']
        hashed_password = sha256_crypt.hash(password)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone_no = request.form['phone_no']
        if len(phone_no)<10 or len(phone_no)>10:
            flash("Invalid Phone no!")
            return redirect(url_for('venregister'))
        for ch in phone_no:
            if not ch.isdigit():
                flash("Invalid Phone no!")
                return redirect(url_for('venregister'))
        vendor = Vendor(Title = title,
                    Password = hashed_password,
                    PhoneNumber = phone_no,
                    FirstName = firstname,
                    LastName = lastname)
        # print vendor.VendorId
        db.session.add(vendor)
        db.session.commit()
        db.session.close()
        flash("Successfully registered!")
        return redirect(url_for('venlogin'))

@app.route('/api/getvenorders/<int:VendorId>/')
def getvenorders(VendorId):
    orders = Orders.query.filter_by(VendorId=VendorId).all()
    return jsonify(orders)    

@app.route('/venprofile/<int:VendorId>/')
def venprofile(VendorId):
    if 'VendorId' in session and session['VendorId'] == VendorId:
        orders = Orders.query.filter_by(VendorId=VendorId).all()
        products = Products.query.filter_by(VendorId=VendorId).all()
        return render_template("venprofile.html", req = orders, products = products, logged_in = True)
    else:
        products = Products.query.filter_by(VendorId=VendorId).all()
        # orders = Orders.query.filter_by(VendorId=VendorId).all()
        return render_template("venprofile.html", req = products, logged_in = False)

            

########## Order ###########

@app.route('/addorder/<int:pid>', methods=['POST','GET'])
def addorder(pid):
    if request.method == "GET":
        return render_template("addorder.html")
    else:
        order_time = time.strftime('%Y-%m-%d %H:%M:%S')
        quantity = request.form['quantity']
        product = Products.query.filter_by(ProductId=pid).first()
        vid = product.VendorId
        status = "pending"
        order = Orders(VendorId = vid, 
        ProductId = pid,
        UserId = session['UserId'],
        Status = status,
        Quantity = quantity,
        OrderAt = order_time)
        db.session.add(order)
        db.session.commit()
        db.session.close()
    return redirect(url_for('userprofile',uid = session['UserId']))

@app.route('/orderdetail/<int:oid>')
def orderdetail(oid):
    order = Orders.query.filter_by(OrderId=oid).first()
    productid = order.ProductId
    product = Products.query.filter_by(ProductId=productid).first()
    return render_template('orderdetail.html', order = order, product = product)


########## Products ###########

@app.route('/addproduct', methods=['POST','GET'])
def addproduct():
    if request.method == "GET":
        return render_template("addproduct.html")
    else:
        productname = request.form['productname']
        productprice = request.form['productprice']
        product = Products(ProductName = productname,
        ProductPrice = productprice,
        VendorId = session['VendorId'])
        db.session.add(product)
        db.session.commit()
        db.session.close()
    return redirect(url_for('homepage'))

########## Search ##########

@app.route('/search', methods=['POST'])
def search():
    query = request.form['search_query']
    vendors = Vendor.query.filter(Vendor.Title.contains(query))
    user = User.query.filter_by(UserId = session['UserId']).first_or_404()
    return render_template("userProfile.html",user=user,vendors=vendors)

