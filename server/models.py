from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin


from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-recipes.user', '-_password_hash')

    id = db.Column(db.Integer, primary_key = True)
    # username that is a String type.
    username = db.Column(db.String, unique=True, nullable=False)
    # _password_hash that is a String type.
    _password_hash = db.Column(db.String)
    # image_url that is a String type.
    image_url = db.Column(db.String)
    # bio that is a String type.
    bio = db.Column(db.String)
    # recipes 
    recipes = db.relationship('Recipe', back_populates='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash =  bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    __table_args__ = (
        db.CheckConstraint('length(instructions) >= 50'),  
    )

    id = db.Column(db.Integer, primary_key = True)
    # title that is a String type.
    # title must be present.
    title = db.Column(db.String, nullable = False)
    # instructions that is a String type.
    instructions = db.Column(db.String, nullable = False)
    # minutes_to_complete that is an Integer type.
    minutes_to_complete = db.Column(db.Integer)
    # user_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='recipes')

    def __repr__(self):
            return f'<Recipe {self.title}>'