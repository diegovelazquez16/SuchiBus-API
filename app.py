from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Importa Flask-CORS
from dotenv import load_dotenv  # Importa load_dotenv de dotenv
import os  # Importa os para acceder a las variables de entorno
from config import config
from src.routes.userRoutes import usuario_blueprint
from src.routes.terminalRoutes import terminal_blueprint
from src.routes.unidadRoutes import unidad_blueprint  # Asegúrate de importar el blueprint de unidades
from src.models.user import db

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    # Configurar SQLAlchemy con la variable de entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Opcional, si deseas desactivar las notificaciones de modificación

    # Habilitar CORS para todas las rutas
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

    db.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    # Registrar Blueprints
    app.register_blueprint(usuario_blueprint)
    app.register_blueprint(terminal_blueprint)
    app.register_blueprint(unidad_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
