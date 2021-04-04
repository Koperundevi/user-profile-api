# Import all the required modules/packages
from models import User, db
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

'''
 Get User using jwt identity
'''

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        userObj = User.query.get(get_jwt_identity())
        return userObj.__repr__() if userObj else {}

