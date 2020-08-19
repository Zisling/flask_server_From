from flask import Flask, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# import users

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SECRET KEY
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET'])
def index():
    username = request.json['username']
    if username in session:
        return jsonify({'user_state': 'Logged in as %s' % session[username]})
    return jsonify({'user_state': 'You are not logged in'})


@app.route('/login/<username>', methods=['POST'])
def login(username):
    session[username] = username
    return {'user_state': 'Logged in as %s' % session[username]}


@app.route('/logout' , methods=['PUT'])
def logout():
    # remove the username from the session if it's there
    username = request.json['username']
    session.pop(username, None)
    return jsonify({'user_state': 'You are logged out {}'.format(username) })


# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    print(result)
    return jsonify(result)


@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    return product_schema.jsonify(product)


@app.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.qty = request.json['qty']
    db.session.commit()
    return product_schema.jsonify(product)


@app.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


# run server
if __name__ == '__main__':
    app.run(port=5000, debug=True)
