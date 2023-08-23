from flask import Flask, jsonify, render_template
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException, default_exceptions
import settings

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# API ROUTING
api = Api(app)
api.prefix = '/api'

from endpoints.roles.resource import RolesResource
from endpoints.users.resource import UsersResource

api.add_resource(RolesResource, '/role', '/role/<int:product_id>')
api.add_resource(UsersResource, '/user', '/user/<int:order_id>')

@app.route('/api/login', methods=['POST'])
def invoke_login():
    users_resource = UsersResource()
    return users_resource.login()

# PAGE ROUTING
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()
