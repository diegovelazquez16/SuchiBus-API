import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de autenticación JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Configuración de Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_CREDENTIALS_PATH')

if SERVICE_ACCOUNT_FILE:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build('drive', 'v3', credentials=credentials)
else:
    drive_service = None
    print("No se encontraron las credenciales de Google Drive.")

# Configuración del entorno
class Config:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = SQLALCHEMY_TRACK_MODIFICATIONS
    JWT_SECRET_KEY = JWT_SECRET_KEY

config = {
    'development': Config,
    'testing': Config
}