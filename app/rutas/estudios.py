from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from db import db
from modelos.estudio import Estudio

estudio_bp = Blueprint("estudio", __name__)

@estudio_bp.route('/estudios', methods=['POST'])
@jwt_required()
def crear_estudio():
  datos = request.get_json()
  
  if not datos or "nombre" not in datos:
    return jsonify({"error": "Faltan datos"}), 400
  
  estudio = Estudio.query.filter(Estudio.nombre == datos["nombre"]).first()
  if estudio:
    return jsonify({"error": "Ya existe el estudio"}), 409
  
  descripcion = datos.get("descripcion", "")
  if not descripcion:
    descripcion = ""
  
  nuevo_estudio = Estudio(
    nombre = datos["nombre"],
    descripcion = descripcion
  )
  
  try:
    db.session.add(nuevo_estudio)
    db.session.commit()
    return jsonify({"mensaje": "Estudio creado"}), 201
  except Exception as exception:
    db.session.rollback()
    return jsonify({"error": str(exception)}), 500

@estudio_bp.route('/estudios', methods=['GET'])
def get_estudios():
  estudios = Estudio.query.filter().all()
  
  if len(estudios) == 0:
    return jsonify([]), 200

  resultado = []
  for estudio in estudios:
    resultado.append({
      "id": estudio.id,
      "nombre": estudio.nombre,
      "descripcion": estudio.descripcion
    })
  
  return jsonify(resultado), 200

@estudio_bp.route('/estudios/<int:id>', methods=['DELETE'])
@jwt_required()
def borrar_estudio(id):
  estudio = Estudio.query.get(id)
  
  if not estudio:
    return jsonify({"error": "No existe el estudio"}), 404
  
  try:
    db.session.delete(estudio)
    db.session.commit()
    return jsonify({"mensaje": "Estudio borrado"}), 200
  except Exception as exception:
    db.session.rollback()
    return jsonify({"error": str(exception)}), 500