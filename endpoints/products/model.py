from app import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(50))
    price = db.Column(db.Integer)

    orders = db.relationship('Order', backref='product', lazy='select')

    def __repr__(self):
        return 'Id: {}, name: {}, description: {}, price: {}'.format(self.id, self.name, self.description, self.price)