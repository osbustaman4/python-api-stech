import traceback

# Database
from src.database.db_mysql import get_connection


from src.models.ObjectData import ObjectData
from src.utils.Logger import Logger


class ObjectDataService():

    @classmethod
    def get_data(cls):
        try:
            connection = get_connection()
            objectsData = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM gs_object_data_356028083510025')
                resulset = cursor.fetchall()
                for row in resulset:
                    objectData = ObjectData((row[0]).strftime('%d/%m/%Y %H:%M:%S'), (row[1]).strftime('%d/%m/%Y %H:%M:%S'), str(
                        row[2]), str(row[3]), float(row[4]), float(row[5]), float(row[6]), str(row[7]), float(row[8]))
                    objectsData.append(objectData.to_json())
                connection.close()
                return objectsData

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
