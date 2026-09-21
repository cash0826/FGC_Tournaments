from config import Config
from flask import Flask
from extensions import db, migrate, api


def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  
  # initialize extensions
  db.init_app(app)
  migrate.init_app(app, db)
  # bcrypt.init_app(app)
  # jwt.init_app(app)
  api.init_app(app)
  
  # import models
  from models.user import User
  from models.role import Role
  from models.user_role import UserRole
  
  # import resources
   # TODO: from controllers import Auth
  
  with app.app_context():
    db.create_all()
  
  return app
  
if __name__ == "__main__":
  app = create_app()
  app.run(debug=True, port=5555)
