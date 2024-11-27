from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from src.routes.userRoutes import usuario_blueprint
from src.routes.terminalRoutes import terminal_blueprint
from src.routes.unidadRoutes import unidad_blueprint
from src.routes.drive_Routes import drive_bp
from src.models.user import db
from config import config

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de CORS para permitir solicitudes desde el dominio y la IP especificados
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
    
    cors_options = {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],   
        "allowed_headers": ["Content-Type", "Authorization"]
        }


    db.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(usuario_blueprint)
    app.register_blueprint(terminal_blueprint)
    app.register_blueprint(unidad_blueprint)
    app.register_blueprint(drive_bp)

    return app

app = create_app()  

if __name__ == '__main__':
    app.run(debug=True)
