from config import db

class Orders(db.Model):
    __tablename__ = "orders"
    OrderId = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    ProductId = db.Column(db.Integer, nullable=False)
    UserId = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    OrderAt = db.Column(db.DateTime, nullable=False)




