from flask import Flask
from .extensions import db, migrate
from .routes import main_bp  # HTML routes and dashboard

# Optional: Import this only if you're using SQLAlchemy models
# from .models import *

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprint for main routes
    app.register_blueprint(main_bp)

    return app

