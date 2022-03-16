from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }



class Character (db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column (db.String(50), nullable=False)
    birth_year=db.Column(db.String(10), nullable=True)
    gender=db.Column(db.String(25), nullable=True)
    height=db.Column(db.Float, nullable=True)
    skin_color=db.Column(db.String(25),nullable=False)
    hair_color=db.Column(db.String(25), nullable=False)
    eye_color=db.Column(db.String(25),nullable=False)
    description=db.Column(db.String(300),nullable=False)
    photo_url=db.Column(db.String(300),nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year":self.birth_year,
            "gender":self.gender,
            "height":self.height,
            "skin_color":self.skin_color,
            "hair_color":self.hair_color,
            "eye_color":self.eye_color,
            "description":self.description,
            "photo_url":self.photo_url,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    name = db.Column(db.String(50), nullable=False)     
    climate = db.Column(db.String(25), nullable=False)     
    terrain = db.Column(db.String(25), nullable=False)     
    population = db.Column(db.Integer, nullable=True)     
    orbital_period = db.Column(db.Float, nullable=False)     
    rotation_period = db.Column(db.Float, nullable=False)     
    diameter = db.Column(db.Float, nullable=False)     
    description = db.Column(db.String(300), nullable=False)     
    photo_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate":self.climate,
            "terrain":self.terrain,
            "population":self.population,
            "orbital_period":self.orbital_period,
            "rotation_period":self.rotation_period,
            "diameter":self.diameter,
            "photo_url":self.photo_url,
            
        }

class Character_Fav(db.Model):
        
    id= db.Column(db.Integer, primary_key=True)
    id_user= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id_character= db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    user = db.relationship('User')
    character= db.relationship('Character')       


    def __repr__(self):
        return '<Character-Fav %r>' % self.id

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_user,
            "id_character": self.id_character,
        }

class Planet_Fav(db.Model):
        
    id= db.Column(db.Integer, primary_key=True)
    id_user= db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id_planet= db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
    user = db.relationship('User')
    planet= db.relationship('Planet')       


    def __repr__(self):
        return '<Planet-Fav %r>' % self.id

    def serialize(self):
        return {
            "id":self.id,
            "id_user": self.id_user,
            "id_planet": self.id_planet,
        }   