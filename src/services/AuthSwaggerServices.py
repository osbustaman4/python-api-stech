import traceback
from src.models.AuthUser.User import User

from src.utils.Logger import Logger

from src.database.db_mysql import get_connection
from flask_swagger_ui import get_swaggerui_blueprint

class AuthSwaggerServices():

    CONNECTION = get_connection()

    @classmethod
    def loginSwagger(self, data):

        username = data['username']
        password = data['password']

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM gs_users WHERE username = '{ username }' AND password = MD5('{ password }');""")
                result = cursor._rows

                if result:
                    user = User(result[0][0], result[0][1], result[0][2])
                    return user

                return False  # Si no se encuentra el usuario

            
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            with cls.CONNECTION.cursor() as cursor:
                cursor.execute(f"SELECT id, username, password  FROM gs_users WHERE id = {user_id}")
                result = cursor._rows

                if result:
                    user = User(result[0][0], result[0][1], result[0][2])
                    return user

            return False  # Si no se encuentra el usuario

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None  # En caso de error


    @classmethod
    def initSwagger(self, initSwagger = False):

        if initSwagger:
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
        
        else:
            SWAGGER_URL = '/swagger'
            SWAGGER_BLUEPRINT = False

        return SWAGGER_BLUEPRINT, SWAGGER_URL