from marshmallow import Schema, fields
from models import Profile

'''Profile schema'''

class ProfileSchema(Schema):
    class Meta:
        model = Profile
    name = fields.String()
    phone = fields.String()
    email = fields.String()
    currentaddress = fields.String()
    previousaddress = fields.String()