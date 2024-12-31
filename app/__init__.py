from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_routes
    from app.routes.employee import employee_bp
    from app.routes.shift import shift_bp

    app.register_blueprint(auth_routes)
    app.register_blueprint(employee_bp)
    app.register_blueprint(shift_bp)



    return app
