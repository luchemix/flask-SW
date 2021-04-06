"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Planets, People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def getUser():

    user_query = User.query.all()
    all_users = list(map(lambda x: x.serialize(), user_query))

    return jsonify(all_users), 200

@app.route('/fav', methods=['GET'])
def getFav():

    fav_query = Favorites.query.all()
    all_favs = list(map(lambda x: x.serialize(), fav_query))
    return jsonify(all_favs), 200

@app.route('/planet', methods=['GET'])
def getPlanet():

    planet_query = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planet_query))
    return jsonify(all_planets), 200

@app.route('/planet/<int:plid>', methods=['GET'])
def getPlanetId(plid):

    planet = Planets.query.get(plid)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    result = planet.serialize()
    return jsonify(result), 200

@app.route('/people/<int:pid>', methods=['GET'])
def getPeopleId(pid):

    person = People.query.get(pid)
    if person is None:
        raise APIException('Person not found', status_code=404)
    result = person.serialize()
    return jsonify(result), 200

@app.route('/user/<int:uid>/fav/', methods=['GET'])
def getUserFavs(uid):

    user = User.query.filter_by(id=uid).first()
    if user is None:
        raise APIException('User favorites not found', status_code=404)
    fav = Favorites.query.filter_by(user_id=uid).first()
    result = fav.serialize()
    return jsonify(result), 200


# @app.route('/user/<int:uid>/fav/', methods=['POST'])
# def postUserFavs(uid):

#     request_body = request.get_json()
#     fav = Favorites(name=request_body["name"])
#     db.session.add(fav)
#     db.session.commit()

#     return jsonify(fav), 200

    
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
