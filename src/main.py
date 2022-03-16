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
from models import db, User, Character_Fav, Character,Planet,Planet_Fav
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])   
def listCharacters():
    list_characters= Character.query.all()
    return jsonify([character.serialize() for character in list_characters])

@app.route('/characters/<int:character_id>', methods=['GET']) 
def getCharacter(character_id):     
    char = Character.query.filter_by(id=character_id).first()     #Coger especificamente un id de un url
    return jsonify(char.serialize()), 200

@app.route('/planets', methods=['GET'])   
def listPlanets():
    list_planets= Planet.query.all()
    return jsonify([planet.serialize() for planet in list_planets])    

@app.route('/planets/<int:planet_id>', methods=['GET']) 
def getPlanet(planet_id):     
    planet = Planet.query.filter_by(id=planet_id).first()     
    return jsonify(planet.serialize()), 200    

@app.route('/users', methods=['GET'])   
def listusers():
    list_users= User.query.all()
    return jsonify([user.serialize() for user in list_users])

@app.route('/users/<int:user_id>', methods=['GET']) 
def getUser(user_id):     
    user = User.query.filter_by(id=user_id).first()     
    return jsonify(user.serialize()), 200     

@app.route('/users/<int:user_id>/favorites', methods=['GET'])   
def listUsersFavorites():
    user = User.query.filter_by(id=user_id).first()  
    favorites= query.all(Fav_Charaters,Fav_Planets)
    return jsonify([user.serialize() for user in list_users])    

@app.route('/favorite/planet/<int:planet_id>', methods=['POST']) 
def create_favorite_planet(planet_id):
   
    user=request.json.get("user")
    
    
    favPlanet= Planet_Fav(id_planet=planet_id, id_user=user)     

    db.session.add(favPlanet)
    db.session.commit()   
    return jsonify({"message" : "Favorito de planeta creado correctamente"}), 200
     
@app.route('/favorite/people/<int:people_id>', methods=['POST']) 
def create_favorite_people(people_id):
   
    user=request.json.get("user")
    
    
    favPeople= Character_Fav(id_character=people_id, id_user=user)     

    db.session.add(favPeople)
    db.session.commit()   
    return jsonify({"message" : "Favorito de personaje creado correctamente"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])

def delete_favorite_planet(planet_id):

    user=request.json.get("user")      
    favorite_planet = Planet_Fav.query.filter_by(id_planet=planet_id, id_user=user).first() 

    if not favorite_planet:
            return jsonify({"message": "El Favorito de planeta no fue encontrado"}), 400
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({"message" : "El Favorito de planeta fue borrado con éxito"}), 200    

@app.route('/favorite/characters/<int:character_id>', methods=['DELETE'])

def delete_favorite_people(character_id):

    user=request.json.get("user")      
    favorite_character = Character_Fav.query.filter_by(id_character=character_id, id_user=user).first() 

    if not favorite_character:
            return jsonify({"message": "El Favorito de personaje no fue encontrado"}), 400
    db.session.delete(favorite_character)
    db.session.commit()
    return jsonify({"message" : "El Favorito de personaje fue borrado con éxito"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)