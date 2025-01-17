from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['JSON_AS_ASCII'] = False  # Prevents ASCII encoding for JSON responses

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_routes
    from app.routes.employee import employee_bp
    from app.routes.shift import shift_bp
    from app.routes.jobTitle import job_title_bp
    from app.routes.attendance import attendance_bp

    app.register_blueprint(auth_routes)
    app.register_blueprint(employee_bp)
    app.register_blueprint(shift_bp)
    app.register_blueprint(job_title_bp)
    app.register_blueprint(attendance_bp)



    return app
