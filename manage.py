# Import all the required modules/packages
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from models import db

'''Initialize Migrate,
use: to migrate the model changes to the database'''

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()