from flask import Flask

from src.routes import ObjectDataRoutes

app = Flask(__name__)

def init_app(config):

    app.config.from_object(config)

    app.register_blueprint(ObjectDataRoutes.main_get_data, url_prefix='/')
    app.register_blueprint(ObjectDataRoutes.main_getObjectData, url_prefix='/object-data/base64')
    app.register_blueprint(ObjectDataRoutes.main_getObjectDataJson, url_prefix='/object-data/json')

    return app