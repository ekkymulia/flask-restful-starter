from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import Product
from app import db

product_fields = {
    'id': fields.Integer,
    'name' : fields.String,
    'description' : fields.String,
    'price' : fields.String
}

product_list_fields = {
    'count': fields.Integer,
    'todos': fields.List(fields.Nested(product_fields)),
}

product_post_parser = reqparse.RequestParser()
product_post_parser.add_argument('name', type=str, required=True, location=['json'],
                              help='name parameter is required')
product_post_parser.add_argument('description', type=str, required=True, location=['json'],
                              help='description parameter is required')
product_post_parser.add_argument('price', type=int, required=True, location=['json'],
                              help='price parameter is required')


class ProductsResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.filter_by(id=product_id).first()
            return marshal(product, product_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            product = Product.query.filter_by(**args).order_by(product_id)
            if limit:
                product = product.limit(limit)

            if offset:
                product = product.offset(offset)

            product = product.all()

            return marshal({
                'count': len(product),
                'todos': [marshal(t, product_fields) for t in product]
            }, product_list_fields)

    @marshal_with(product_fields)
    def post(self):
        args = product_post_parser.parse_args()

        # mass assignment method
        product = Product(**args)
        db.session.add(product)
        db.session.commit()

        return product

    @marshal_with(product_fields)
    def put(self, product_id=None):
        product = Product.query.get(product_id)

        # prevent mass assignment
        if 'name' in request.json:
            product.name = request.json['name']

        if 'description' in request.json:
            product.description = request.json['description']

        # if 'total_price' in request.json:
        #     product.total_price = request.json['total_price']

        if 'price' in request.json:
            product.price = request.json['price']

        # allow mass assignment
        # product = request.json

        db.session.commit()
        return product

    @marshal_with(product_fields)
    def delete(self, product_id=None):
        product = Product.query.get(product_id)

        db.session.delete(product)
        db.session.commit()

        return product