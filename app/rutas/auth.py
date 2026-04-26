from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from modelos.usuario import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/registro', methods=['POST'])
def registro():
  datos = request.get_json()
  
  datos_necesarios = ["nombre", "apellidos", "email", "password"]
  if not datos or not all(campo in datos for campo in datos_necesarios):
    return jsonify({"error": "Faltan datos"}), 400
  
  email = datos.get("email")
  usuario = Usuario.query.filter(Usuario.email == email).first()
  if usuario:
    return jsonify({"error": "usuario ya registrado"}), 409
  
  password_hash = generate_password_hash(datos["password"])
  
  nuevo_usuario = Usuario(
    nombre = datos["nombre"],
    apellidos = datos["apellidos"],
    email = datos["email"],
    password = password_hash
  )
  
  try:
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado"}), 201
  except Exception as exception:
    db.session.rollback()
    return jsonify({"error": str(exception)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
  datos = request.get_json()
  
  if not datos or "email" not in datos or 'password' not in datos:
    return jsonify({"message": "Faltan datos obligatorios"}), 400
  
  usuario = Usuario.query.filter(Usuario.email == datos["email"]).first()
  if not usuario or not check_password_hash(usuario.password, datos["password"]):
    return jsonify({"error": "Datos incorrectos"}), 401
  
  token = create_access_token(identity=str(usuario.id))
  respuesta = make_response(jsonify({"token": token}), 200)
  return respuesta