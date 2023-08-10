
import traceback

from src.database.db_mysql import get_connection
from src.utils.Logger import Logger
from src.models.auth.Auth import Auth

class AuthServices():
    CONNECTION = get_connection()


    @classmethod
    def loginUser(self, data):

        username = data['username']
        password = data['password']

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM gs_users WHERE username = '{ username }' AND password = MD5('{ password }');""")
                result = cursor._rows

                if result:
                    user = Auth(result[0][0], result[0][1], result[0][2])
                    return user

                return False  # Si no se encuentra el usuario

            
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


    @classmethod
    def getUserById(self, data):

        user_id = data['user_id']

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"SELECT id, username, password  FROM gs_users WHERE id = {user_id}")
                result = cursor._rows

                if result:
                    user = Auth(result[0][0], result[0][1], result[0][2])
                    return user

            return False  # Si no se encuentra el usuario

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None  # En caso de error