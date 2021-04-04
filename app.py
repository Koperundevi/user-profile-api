# Import all the required modules/packages
from flask import Flask
import logging, sys
from flask_restful import Api
from models import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import getEnvConfig

#Initialize the flask app
app = Flask(__name__)

#Update the app config by getting the env config
config = getEnvConfig()
app.config.from_object(config)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

#Initialize JWT
jwt = JWTManager(app)

#Initialize rest api
restApi = Api(app)

#Initialize db app
db.init_app(app)

#Add the blueprint from routes and initalizing rest resource
from routes import routeApp, initialize_routes
app.register_blueprint(routeApp)
initialize_routes(restApi)

#Initialize CORS
CORS(app)

if __name__ == '__main__':
    app.run(host = config.FLASK_RUN_HOST, port = config.FLASK_RUN_PORT, debug = config.DEBUG)