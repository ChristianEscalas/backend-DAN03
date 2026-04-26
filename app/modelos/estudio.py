from db import db

class Estudio(db.Model):
  __tablename__ = "estudios"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  nombre = db.Column(db.String(100), nullable = False)
  descripcion = db.Column(db.Text, nullable = True)
  
  profesores = db.relationship("Profesor", back_populates = "estudio")