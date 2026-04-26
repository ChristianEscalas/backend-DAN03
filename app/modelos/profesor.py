from db import db

class Profesor(db.Model):
  __tablename__ = "profesores"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable = False)
  estudio_id = db.Column(db.Integer, db.ForeignKey("estudios.id"), nullable = False)
  
  usuario = db.relationship("Usuario", back_populates = "profesores")
  estudio = db.relationship("Estudio", back_populates = "profesores")