from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from db import db
import os
# Carga de variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Instancia y configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configuración y conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
jwt = JWTManager(app)

# Blueprints
from rutas.auth import auth_bp
from rutas.profesores import profesor_bp
from rutas.estudios import estudio_bp

# Registrar rutas
app.register_blueprint(auth_bp)
app.register_blueprint(profesor_bp)
app.register_blueprint(estudio_bp)
# Configuración de JWT y expiración en 2 horas
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True)