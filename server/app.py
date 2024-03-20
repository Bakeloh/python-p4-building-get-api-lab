#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "baked_goods": [BakedGood.query.filter_by(bakery_id=bakery.id).first().to_dict()],
            "created_at": bakery.created_at,
            "id": bakery.id,
            "name": bakery.name,
            "updated_at": bakery.updated_at,
        }
        bakeries_list.append(bakery_dict)
    response = make_response(
        jsonify(bakeries_list), 200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        bakery_dict = bakery.to_dict()
        response = make_response(
            jsonify(bakery_dict), 200
        )
        response.headers["Content-Type"] = "application/json"
    else:
        response = make_response(
            jsonify({"error": "Bakery not found"}), 404
        )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bakes = []
    for baked in BakedGood.query.order_by(BakedGood.price.desc()).all():
        baked_dict = {
            "bakery_id": baked.bakery_id,
            "created_at": baked.created_at,
            "id": baked.id,
            "name": baked.name,
            "price": baked.price,
            "updated_at": baked.updated_at,
        }
        bakes.append(baked_dict)
    response = make_response(
        jsonify(bakes), 200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked:
        baked_dict = baked.to_dict()
        response = make_response(
            jsonify(baked_dict), 200
        )
        response.headers["Content-Type"] = "application/json"
    else:
        response = make_response(
            jsonify({"error": "No baked goods found"}), 404
        )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)