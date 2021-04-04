from flask import Blueprint

routeApp = Blueprint('routeApp', __name__)
from service import home, api

'''Declare the routes of app'''

def initialize_routes(restApi):
    #Declare Resource
    restApi.add_resource(api.UserProfile, '/user/me')
    restApi.add_resource(api.ProfileDetails, '/profile')

routeApp.add_url_rule('/', view_func=home.index)
routeApp.add_url_rule('/login', view_func=home.login)
routeApp.add_url_rule('/login/callback', view_func=home.callback)