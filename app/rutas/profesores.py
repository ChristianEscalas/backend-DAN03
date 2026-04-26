from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from db import db
from modelos.estudio import Estudio
from modelos.profesor import Profesor
from modelos.usuario import Usuario

profesor_bp = Blueprint("profesor", __name__)

@profesor_bp.route('/profesores', methods=['POST'])
@jwt_required()
def crear_profesor():
  datos = request.get_json()
  
  datos_necesarios = ["usuario_id", "estudio_id"]
  if not datos or not all(campo in datos for campo in datos_necesarios):
    return jsonify({"error": "Faltan datos"}), 400
  
  usuario = Usuario.query.get(datos["usuario_id"])
  if not usuario:
    return jsonify({"error": "No existe el usuario"}), 404
  
  estudio = Estudio.query.get(datos["estudio_id"])
  if not estudio:
    return jsonify({"error": "No existe el estudio"}), 404
  
  nuevo_profesor = Profesor(
    usuario_id = usuario.id,
    estudio_id = estudio.id
  )
  
  try:
    db.session.add(nuevo_profesor)
    db.session.commit()
    return jsonify({"mensaje": "Profesor creado"}), 201
  except Exception as exception:
    db.session.rollback()
    return jsonify({"error": str(exception)}), 500

@profesor_bp.route('/profesores', methods=['GET'])
def get_profesores():
  profesores = Profesor.query.filter().all()
  
  if len(profesores) == 0:
    return jsonify([]), 200

  resultado = []
  for profesor in profesores:
    resultado.append({
      "id": profesor.id,
      "nombre": profesor.usuario.nombre,
      "apellidos": profesor.usuario.apellidos,
      "email": profesor.usuario.email,
      "especialidad": profesor.estudio.nombre
    })
  
  return jsonify(resultado), 200

@profesor_bp.route('/profesores/<int:id>', methods=['DELETE'])
@jwt_required()
def borrar_profesor(id):
  profesor = Profesor.query.get(id)
  
  if not profesor:
    return jsonify({"error": "No existe el profesor"}), 404
  
  try:
    db.session.delete(profesor)
    db.session.commit()
    return jsonify({"mensaje": "Profesor borrado"}), 200
  except Exception as exception:
    db.session.rollback()
    return jsonify({"error": str(exception)}), 500