from datetime import timedelta
import sys, os

'''get config based on environment'''
def getEnvConfig():
    env = os.getenv('FLASK_ENV')
    return app_config[env] if env else DevelopmentConfig

class Config(object):
    """
    Common configurations
    """
    PROPAGATE_EXCEPTIONS = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SQLALCHEMY_ECHO = False
    DEBUG = True
    #github authorization URI
    GITHUB_AUTH_URI = """https://github.com/login/oauth/authorize?response_type=code&client_id=5a429afe708ee411ec8f&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Flogin%2Fcallback&scope=user"""
    #postgresql://user:pw@host:port/db
    SQLALCHEMY_DATABASE_URI = """postgresql://postgres:postgres@localhost:5432/userprofileapp"""
    #github access token header
    GITHUB_ACCESS_TOKEN_HEADER = {"client_id": "5a429afe708ee411ec8f",
        "client_secret": "a927daabebe346f36a27bf75aa0a0de99d487d34",
        "code":""
        }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_SECRET_KEY = 'a927daabebe346f36a27bf75aa0a0de99d487d34'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=10)
    FLASK_RUN_HOST = '127.0.0.1'
    FLASK_RUN_PORT = 8000
    LOGIN_SUCCESS_REDIRECT_URI = "http://localhost:4200/profile?token="
    
class ProductionConfig(Config):
    """
    Production configurations
    """

    SQLALCHEMY_ECHO = False
    DEBUG = False
    #github authorization URI
    GITHUB_AUTH_URI = """https://github.com/login/oauth/authorize?response_type=code&client_id=90b8b080bb9c3ac59350&redirect_uri=http%3A%2F%2Fuser-profile-api.herokuapp.com%2Flogin%2Fcallback&scope=user"""
    #postgresql://user:pw@host:port/db
    SQLALCHEMY_DATABASE_URI = """postgresql://tozpjdfkrgpjjd:b1f7915e9f8574f731d58214ca6a76e5d8a95999869fd37cb8575f3889824e59@ec2-52-45-73-150.compute-1.amazonaws.com:5432/dccoog9uvjg7bg"""
    #github access token header
    GITHUB_ACCESS_TOKEN_HEADER = {"client_id": "90b8b080bb9c3ac59350",
        "client_secret": "e84f6c8fe2ed62d024eaa13c3e743bee1653589c",
        "code":""
        }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JWT_SECRET_KEY = 'e84f6c8fe2ed62d024eaa13c3e743bee1653589c'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=5)
    FLASK_RUN_HOST = '0.0.0.0'
    FLASK_RUN_PORT=5000
    LOGIN_SUCCESS_REDIRECT_URI = "https://user-profile-appln.herokuapp.com/profile?token="

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
