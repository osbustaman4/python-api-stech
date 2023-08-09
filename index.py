from app_config import configure
from src import init_app

from flask_login import LoginManager

from src.services.AuthSwaggerServices import AuthSwaggerServices

configuration = configure['development']
app = init_app(configuration)


# Configurar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "main_mainSwaggerOauth.login_page"


@login_manager.user_loader
def load_user(user_id):
    # Aquí debes implementar la recuperación del usuario de tu sistema de autenticación
    # Usando el ID de usuario cargado desde la sesión
    user = AuthSwaggerServices.get_user_by_id(user_id)
    
    return user

# Agregar esta línea para definir la variable 'application'
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)