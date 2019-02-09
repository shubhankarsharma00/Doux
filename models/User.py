from config import db

class User(db.Model):
    __tablename__ = "user"
    UserId = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    RollNumber = db.Column(db.Integer, unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(10), nullable=False)




