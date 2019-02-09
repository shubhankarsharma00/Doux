from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:jkl;'@localhost/doux"
db = SQLAlchemy(app)
app.secret_key = 'random secret key'
