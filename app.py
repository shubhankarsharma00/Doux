from flask import *
from flask_sqlalchemy import *
from config import *

@app.route('/')
def homepage():
	return render_template("index.html")

@app.route('/login')
def login():
	return render_template("userregister.html")

# @app.route('/login',)
# def login():	
#     if request.method == "GET":
#         return render_template("login.html")
#     else:
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if not(user):
#             flash("This Username doesn't exists!")
#             return redirect(url_for('login'))
#         else:
#             password_correct = sha256_crypt.verify(password, user.password)
#             if not(password_correct):
#                 flash("Wrong password entered!")
#                 return redirect(url_for('login'))
#             else:
#                 flash("Logged in successfully:)")
#                 session['username'] = username
#                 session['u_id'] = user.u_id
#                 session['logged_in'] = True
#         return redirect(url_for('homepage'))
