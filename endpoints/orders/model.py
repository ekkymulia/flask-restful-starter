from app import db
from endpoints.products.model import Product


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String(20))
    description = db.Column(db.String(100))
    total_price = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                        nullable=False)

    def __repr__(self):
        return 'Id: {}, quantity: {}, description: {}, total_price: {}, product_id: {}'.format(self.id, self.quantity, self.description, self.total_price, self.product_id)

    # @property
    # def total_price(self):
    #     # Fetch the corresponding product from the database using the product_id
    #     product = Product.query.get(self.product_id)
    #
    #     # Calculate the total price based on quantity and product price
    #     if product:
    #         return int(self.quantity) * product.price
    #
    #     return 0
