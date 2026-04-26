from db import db

class Usuario(db.Model):
  __tablename__ = "usuarios"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  nombre = db.Column(db.String(30), nullable = False)
  apellidos = db.Column(db.String(50), nullable = False)
  email = db.Column(db.String(100), unique = True, nullable = False)
  password = db.Column(db.String(255), nullable = False)
  
  profesores = db.relationship("Profesor", back_populates = "usuario")