from config import db

class Products(db.Model):
    __tablename__ = "products"
    ProductId = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    ProductName = db.Column(db.String(255), nullable=False)
    VendorId = db.Column(db.Integer, nullable=False)
    ProductPrice = db.Column(db.Integer,nullable=False)




