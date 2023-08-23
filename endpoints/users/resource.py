from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from werkzeug.security import check_password_hash

from .model import User
from app import db

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'role_id': fields.Integer
}

user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields)),
}

user_login_fields = {
    'username': fields.String,
    'password': fields.String,
}

user_login_response_fields = {
    'response': fields.Integer,
    'message': fields.String,
    'user': fields.Nested(user_fields, allow_null=True)  # Use allow_null=True
}



user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True, location=['json'],
                              help='username parameter is required')
user_post_parser.add_argument('password', type=str, required=True, location=['json'],
                              help='password parameter is required')
user_post_parser.add_argument('role_id', type=int, location=['json'],
                              help='role_id parameter is required')


class UsersResource(Resource):

    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return marshal(user, user_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            user = User.query.filter_by(**args).order_by(user_id)
            if limit:
                user = user.limit(limit)

            if offset:
                user = user.offset(offset)

            user = user.all()

            return marshal({
                'count': len(user),
                'users': [marshal(t, user_fields) for t in user]
            }, user_list_fields)

    @marshal_with(user_fields)
    def post(self):
        args = user_post_parser.parse_args()

        # mass assignment method
        user = User(**args)
        db.session.add(user)
        db.session.commit()

        return user

    @marshal_with(user_fields)
    def put(self, user_id=None):
        user = User.query.get(user_id)

        if request.json:
            for key, value in request.json.items():
                if hasattr(user, key):
                    setattr(user, key, value)

        db.session.commit()
        return user

    @marshal_with(user_fields)
    def delete(self, user_id=None):
        user = User.query.get(user_id)

        db.session.delete(user)
        db.session.commit()

        return user

    @marshal_with(user_login_response_fields)
    def login(self):
        data = user_post_parser.parse_args()

        if 'username' not in data or 'password' not in data:
            return {
                'response': 400,
                'user': user_login_fields
            }

        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if not user:
            return {
                'response': 401,
                'message': "Username not found"
            }

        # if not check_password_hash(user.password, password):
        if user.password != password:
            return {
                'response': 401,
                'message': "Invalid password"
            }

        return {
            'response': 200,
            'message': "Login successful",
            'user': user
        }

