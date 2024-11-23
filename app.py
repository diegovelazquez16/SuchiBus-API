from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS 
from config import config
from src.routes.userRoutes import usuario_blueprint
from src.routes.terminalRoutes import terminal_blueprint
from src.routes.unidadRoutes import unidad_blueprint
from src.models.user import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    cors_options = {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],   
        "allowed_headers": ["Content-Type", "Authorization"]  
    }
    CORS(app, resources={r"/*": cors_options})  

    with app.app_context():
        db.create_all()
    app.register_blueprint(usuario_blueprint)
    app.register_blueprint(terminal_blueprint)
    app.register_blueprint(unidad_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
