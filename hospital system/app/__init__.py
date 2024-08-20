#init.py

from flask import Flask,render_template
from flask_migrate import Migrate
import stripe
import paypalrestsdk
from .extensions import db, login_manager, bcrypt
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    # Load configurations from config file
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    # Register blueprints
    app.register_blueprint(main_bp)

    # Error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback session to prevent issues on next DB call
        return render_template('500.html'), 500


