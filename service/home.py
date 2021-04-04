# Import all the required modules/packages
from flask import request, url_for, redirect
import requests
from urllib.parse import parse_qsl
from config import getEnvConfig
from models import User, db
from flask_jwt_extended import create_access_token

#Load the env config
config = getEnvConfig()

'''
Index page of application
to route you to login page
'''
def index():
    return redirect(url_for('routeApp.login'))

'''
Login page of application
route you to gihub login
'''
def login():
    return redirect(config.GITHUB_AUTH_URI)

'''
Call back url from github provider
'''
def callback():
    try:
        #updating code from github to the github access token header
        config.GITHUB_ACCESS_TOKEN_HEADER.update({"code" : request.args.get("code")})
        #requesting access token from github using the code received
        response = requests.get('https://github.com/login/oauth/access_token',\
                                config.GITHUB_ACCESS_TOKEN_HEADER)
        
        #if success, use the access token to get the user details from github
        if response.status_code == 200:
            queryDict =  dict(parse_qsl(response.text))
            userResponse = requests.get(url = 'https://api.github.com/user',\
                                    headers = {"Authorization": "token {}".format(queryDict.get('access_token'))})
            
            #if user response is success, use the details to create user in our application
            if userResponse.status_code == 200:
                userData = userResponse.json()
                userObj = User.query.filter_by(github_id = userData.get('id')).first()
                if not userObj:
                    userObj = User(username = userData.get('login'), github_id = userData.get('id'),\
                                    is_active = True
                    )
                    db.session.add(userObj)
                    db.session.commit()
                '''generating jwt access token for the application and redirect to the client application
                with the access token'''
                access_token = create_access_token(identity = userObj.id)
                return redirect(config.LOGIN_SUCCESS_REDIRECT_URI+access_token)
            else:
                return {"message": "Error in fetching user form github!"}
        else:
            return {"message": "Error in github login!"}
    except Exception as e:
        return {"message":str(e)}