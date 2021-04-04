from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

'''
User model
'''
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    github_id = db.Column(db.Integer(), nullable=False)
    profile = db.relationship('Profile', backref='user', cascade="all,delete", lazy=True)
 
    '''method to return json seralized value from object'''
    def __repr__(self):
        return {
                "username": self.username,
                "id" : self.id,
                "github_id": self.github_id,
                "is_active": self.is_active,
        }

'''
Profile model
'''
class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(120))
    currentaddress = db.Column(db.String(255))
    previousaddress = db.Column(db.String(255))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    '''method to return json seralized value from object'''
    def __repr__(self):
        return {
                "phone": str(self.phone),
                "name": str(self.name),
                "email": self.email,
                "currentaddress": str(self.currentaddress),
                "previousaddress":self.previousaddress,
                "user_id": self.user_id
                }