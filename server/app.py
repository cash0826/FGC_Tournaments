from config import Config
from flask import Flask
from extensions import db, migrate, api
from models import User, Role, UserRole

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  
  # initialize extensions
  db.init_app(app)
  migrate.init_app(app, db)
  # bcrypt.init_app(app)
  # jwt.init_app(app)
  api.init_app(app)
  
  # import resources
   # TODO: from controllers import Auth
  
  return app
  
if __name__ == "__main__":
  app = create_app()
  app.run(debug=True, port=5555)
