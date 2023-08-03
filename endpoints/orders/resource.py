from flask import current_app
from flask_restful import Resource, reqparse, request, abort
from flask_restful import fields, marshal_with, marshal
from .model import Order
from app import db
from ..products.model import Product

order_fields = {
    'id': fields.Integer,
    'quantity' : fields.Integer,
    'description' : fields.String,
    'total_price' : fields.Integer,
    'product_id' : fields.Integer
}

order_list_fields = {
    'count': fields.Integer,
    'todos': fields.List(fields.Nested(order_fields)),
}

order_post_parser = reqparse.RequestParser()
order_post_parser.add_argument('quantity', type=int, required=True, location=['json'],
                              help='quantity parameter is required')
order_post_parser.add_argument('description', type=str, required=True, location=['json'],
                              help='description parameter is required')
order_post_parser.add_argument('product_id', type=int, required=True, location=['json'],
                              help='product_id parameter is required')


class OrdersResource(Resource):
    def get(self, order_id=None):
        if order_id:
            order = Order.query.filter_by(id=order_id).first()
            return marshal(order, order_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            order = Order.query.filter_by(**args).order_by(order_id)
            if limit:
                order = order.limit(limit)

            if offset:
                order = order.offset(offset)

            order = order.all()

            return marshal({
                'count': len(order),
                'todos': [marshal(t, order_fields) for t in order]
            }, order_list_fields)

    @marshal_with(order_fields)
    def post(self):
        args = order_post_parser.parse_args()

        # total_price generator
        product = Product.query.get(args['product_id'])
        if not product:
            abort(404, message='Product not found')

        total_price = args['quantity'] * product.price
        args['total_price'] = total_price

        # mass assignment method
        order = Order(**args)
        db.session.add(order)
        db.session.commit()

        return order

    @marshal_with(order_fields)
    def put(self, order_id=None):
        order = Order.query.get(order_id)

        # prevent mass assignment
        if 'quantity' in request.json:
            order.quantity = request.json['quantity']

        if 'description' in request.json:
            order.description = request.json['description']

        # if 'total_price' in request.json:
        #     order.total_price = request.json['total_price']

        if 'product_id' in request.json:
            order.product_id = request.json['product_id']

        db.session.commit()
        return order

    @marshal_with(order_fields)
    def delete(self, order_id=None):
        order = Order.query.get(order_id)

        db.session.delete(order)
        db.session.commit()

        return order