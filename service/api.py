# Import all the required modules/packages
from flask import request
import requests, json
from models import User, Profile, db
from flask_restful import Resource
from service.validator import ProfileSchema
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity

'''
 Get User using jwt identity
'''

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        userObj = User.query.get(get_jwt_identity())
        return userObj.__repr__() if userObj else {}

'''
 * CRUD Profile
 * @param {json} data Request body
 *'''

class ProfileDetails(Resource):
    '''Schema for validating the input request body'''
    schema = ProfileSchema()

    '''Get profile details:
    Identity will be fetched with jwt token'''
    @jwt_required()
    def get(self):
        profileObj = Profile.query.filter_by(user_id = get_jwt_identity()).first()
        return profileObj.__repr__() if profileObj else {}

    '''Create profile:
    Identity will be fetched with jwt token'''
    @jwt_required()
    def post(self):
        try:
            data = json.loads(request.data)
            self.schema.load(data)
            current_user = get_jwt_identity()
            profileObj = Profile.query.filter_by(user_id = current_user).first()
            if profileObj:
                return {"status":"failed", "message":"Profile already exists"}
            profileObj = Profile(user_id = current_user,
                        phone = data.get('phone',''),
                        name = data.get('name',''),
                        email = data.get('email',''),
                        currentaddress = data.get('currentaddress',''),
                        previousaddress = data.get('previousaddress',''))
            
            db.session.add(profileObj)
            db.session.commit()
            return profileObj.__repr__()

        except Exception as e:
            return json.dumps({'status':'failed', 'error': 'Exception in creating profile - %s'%(e)})
  
    '''Update profile:
    Identity will be fetched with jwt token'''
    @jwt_required()
    def put(self):
        try:
            data = json.loads(request.data)
            self.schema.load(data)
            profileObj = Profile.query.filter_by(user_id = get_jwt_identity()).first()
            if not profileObj:
                return {"status":"failed", "message":"Profile not available for the current user."}

            profileObj.phone = data.get('phone','')
            profileObj.name = data.get('name','')
            profileObj.email = data.get('email','')
            profileObj.currentaddress = data.get('currentaddress','')
            profileObj.previousaddress = data.get('previousaddress','')
            
            db.session.add(profileObj)
            db.session.commit()
            return profileObj.__repr__()
        except Exception as e:
            import traceback
            traceback.print_exc()
            return json.dumps({'status':'failed', 'error': 'Exception in updating profile - %s'%(e)})

    '''Delete profile:
    Identity will be fetched with jwt token'''
    @jwt_required()
    def delete(self):
        profileObj = Profile.query.filter_by(user_id = get_jwt_identity()).first()
        if profileObj:
            db.session.delete(profileObj)
            db.session.commit()
            return {"status": "success"}
        return {"status": "failed", "message":"Profile not available"}

