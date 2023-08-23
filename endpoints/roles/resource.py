from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import Role
from app import db

role_fields = {
    'id': fields.Integer,
    'name' : fields.String,
}

role_list_fields = {
    'count': fields.Integer,
    'roles': fields.List(fields.Nested(role_fields)),
}

role_post_parser = reqparse.RequestParser()
role_post_parser.add_argument('name', type=str, required=True, location=['json'],
                              help='name parameter is required')


class RolesResource(Resource):
    def get(self, role_id=None):
        if role_id:
            role = Role.query.filter_by(id=role_id).first()
            return marshal(role, role_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            role = Role.query.filter_by(**args).order_by(role_id)
            if limit:
                role = role.limit(limit)

            if offset:
                role = role.offset(offset)

            role = role.all()

            return marshal({
                'count': len(role),
                'todos': [marshal(t, role_fields) for t in role]
            }, role_list_fields)

    @marshal_with(role_fields)
    def post(self):
        args = role_post_parser.parse_args()

        # mass assignment method
        role = Role(**args)
        db.session.add(role)
        db.session.commit()

        return role

    @marshal_with(role_fields)
    def put(self, role_id=None):
        role = Role.query.get(role_id)

        # if 'name' in request.json:
        #     role.name = request.json['name']
        #
        # if 'description' in request.json:
        #     role.description = request.json['description']

        # allow mass assignment
        if request.json:
            for key, value in request.json.items():
                if hasattr(role, key):
                    setattr(role, key, value)

        db.session.commit()
        return role

    @marshal_with(role_fields)
    def delete(self, role_id=None):
        role = Role.query.get(role_id)

        db.session.delete(role)
        db.session.commit()

        return role