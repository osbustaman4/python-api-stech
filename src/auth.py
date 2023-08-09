# auth.py

from src.models.AuthUser.User import User
from src.services.AuthSwaggerServices import AuthSwaggerServices

def load_user(user_id):
    # Aquí debes implementar la lógica para cargar el usuario por su ID
    # Puede ser desde una base de datos, un sistema de autenticación, etc.
    
    # Ejemplo:
    user_data = AuthSwaggerServices.get_user_by_id(user_id)
    
    if user_data:
        user = User(user_data['id'], user_data['username'], user_data['password'])
        return user
    else:
        return None
