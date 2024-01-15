#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'


@app.route('/bakeries', methods=['GET', 'POST'])
def bakeries():
    if request.method == 'GET':
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
        return make_response(bakeries, 200)
    elif request.method == 'POST':
        data = request.get_json()
        new_bakery = Bakery(name=data['name'], location=data['location'])
        db.session.add(new_bakery)
        db.session.commit()
        return make_response({'message': 'Bakery created successfully'}, 201)


@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        if bakery:
            bakery_serialized = bakery.to_dict()
            return make_response(bakery_serialized, 200)
        else:
            return make_response({'message': 'Bakery not found'}, 404)
    
    elif request.method == 'PATCH':
        if bakery:
            data = request.get_json()
            bakery.name = data.get('name', bakery.name)
            bakery.location = data.get('location', bakery.location)
            db.session.commit()
            return make_response({'message': 'Bakery updated successfully'}, 200)
        else:
            return make_response({'message': 'Bakery not found'}, 404)

    elif request.method == 'DELETE':
        if bakery:
            db.session.delete(bakery)
            db.session.commit()
            return make_response({'message': 'Bakery deleted successfully'}, 200)
        else:
            return make_response({'message': 'Bakery not found'}, 404)


@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods_list = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(baked_goods_list, 200)
    elif request.method == 'POST':
        data = request.get_json()
        new_baked_good = BakedGood(name=data['name'], price=data['price'])
        db.session.add(new_baked_good)
        db.session.commit()
        return make_response({'message': 'Baked good created successfully'}, 201)

@app.route('/baked_goods/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def baked_good_by_id(id):
    baked_good = BakedGood.query.filter_by(id=id).first()

    if request.method == 'GET':
        if baked_good:
            baked_good_serialized = baked_good.to_dict()
            return make_response(baked_good_serialized, 200)
        else:
            return make_response({'message': 'Baked good not found'}, 404)
    
    elif request.method == 'PATCH':
        if baked_good:
            data = request.get_json()
            baked_good.name = data.get('name', baked_good.name)
            baked_good.price = data.get('price', baked_good.price)
            db.session.commit()
            return make_response({'message': 'Baked good updated successfully'}, 200)
        else:
            return make_response({'message': 'Baked good not found'}, 404)

    elif request.method == 'DELETE':
        if baked_good:
            db.session.delete(baked_good)
            db.session.commit()
            return make_response({'message': 'Baked good deleted successfully'}, 200)
        else:
            return make_response({'message': 'Baked good not found'}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
