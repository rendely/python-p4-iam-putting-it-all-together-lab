#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):

    def post(self):
        data = request.get_json()
        new_user = User(
            username = data.get('username'),
            image_url = data.get('image_url'),
            bio = data.get('bio'),
        )
        new_user.password_hash = data.get('password')
        try:    
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(), 201
        except IntegrityError:
            return {'error': '422'}, 422



class CheckSession(Resource):
    def get(self):
        if not session.get('user_id'):
            return {'error': '401'}, 401
        else:
            user = User.query.filter_by(id = session.get('user_id')).first()
            return user.to_dict(), 200


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username = data.get('username')).first()
        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'error': '401'}, 401

class Logout(Resource):
    def delete(self):
        if session['user_id']:
            session['user_id'] = None
            return {}, 204
        else:
            return {'error': '401'}, 401

class RecipeIndex(Resource):
    def get(self):
        if not session['user_id']:
            return {'error': '401'}, 401
        
        recipes = Recipe.query.filter_by(user_id = session['user_id']).all()
        recipes_json = [r.to_dict() for r in recipes]
        return recipes_json, 200
    
    def post(self):
        if not session['user_id']:
            return {'error': '401'}, 401
        data = request.get_json()
        new_recipe = Recipe(
            title = data.get('title'),
            minutes_to_complete = int(data.get('minutes_to_complete')),
            instructions = data.get('instructions'),
            user_id = session['user_id']
        )
        try: 
            db.session.add(new_recipe)
            db.session.commit()
        except IntegrityError:
            return {'error': '422'}, 422
        return new_recipe.to_dict(), 201


api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
