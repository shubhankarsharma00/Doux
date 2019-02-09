from config import db

class Vendor(db.Model):
    __tablename__ = "vendor"
    VendorId = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255))
    PhoneNumber = db.Column(db.String(10), nullable=False)




