from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.String(50), primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Product {self.product_name}>"

class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.String(50), primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Location {self.location_name}>"

class ProductMovement(db.Model):
    __tablename__ = 'productmovement'
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    from_location_id = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    to_location_id = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    from_location = db.relationship('Location', foreign_keys=[from_location_id], backref='movements_from')
    to_location = db.relationship('Location', foreign_keys=[to_location_id], backref='movements_to')
    product = db.relationship('Product', backref='movements')

    def __repr__(self):
        return f"<ProductMovement {self.movement_id}>"
