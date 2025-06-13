#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):

        plants = [plant.to_dict() for plant in Plant.query.all()]

        response = make_response(
            plants,
            200,
        )

        return response
    
    def post(self):
        # # Option 1: through form
        # new_plant = Plant(
        #     name=request.form['name'],
        #     image=request.form['image'],
        #     price=request.form['price']
        # )

        # # Option 2: through JSON. get_json allows for error handling
        data = request.get_json() # request.json also works, but it's not official. It's a shortcut property that calls get_json() under the hood.
        
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'] # Suppose we have/used db.Nmeric() in our column: Decimal(str(data['price'])) - accurate
        )
        
        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.to_dict()

        response = make_response(
            response_dict,
            201,
        )

        return response
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):

        plant = Plant.query.filter_by(id=id).first().to_dict()

        response = make_response(
            plant,
            200,
        )

        return response

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
