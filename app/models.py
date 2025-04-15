from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin  
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    password = db.Column(db.String(60), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Cliente {self.nombre}>'
    
    