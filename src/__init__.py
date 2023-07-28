from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from src.routes import ObjectDataRoutes

app = Flask(__name__)

# swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "Todo Lista Endpoints"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)


def init_app(config):

    app.config.from_object(config)

    app.register_blueprint(ObjectDataRoutes.main_get_data, url_prefix='/')
    app.register_blueprint(ObjectDataRoutes.main_getObjectData, url_prefix='/object-data/base64')
    app.register_blueprint(ObjectDataRoutes.main_getObjectDataJson, url_prefix='/object-data/json')

    return app