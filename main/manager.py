from main import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

#Um python manager.py db makemigrations und python manager.py db migrate aufrufen zu können

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()