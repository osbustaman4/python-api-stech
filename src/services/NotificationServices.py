import traceback

from src.database.db_mysql import get_connection
from src.models.Notification import Notification
from src.utils.Logger import Logger

class NotificationService():

    CONNECTION = get_connection()

    @classmethod
    def getAllNotificationUser(self, userId):

        try:
            listObjectsNotificactions = []
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""SELECT 
                                    apn.id
                                    ,apn.id_usuario
                                    ,date_add(apn.fecha_generada, interval(SELECT SUBSTRING(timezone, 2, 3) * - 1 FROM gs_users WHERE id = apn.id_usuario) hour) AS 'fecha_generada'
                                    ,date_add(apn.fecha_actualizada, interval(SELECT SUBSTRING(timezone, 2, 3) * - 1 FROM gs_users WHERE id = apn.id_usuario) hour) AS 'fecha_actualizada'
                                    ,apn.detalle
                                    ,apn.leida
                                    ,apn.oculta
                                    ,apn.tipo
                                    ,apn.imei_vehiculo
                                    ,apn.identificador_tipo
                                    ,apn.contador_reenvios
                                FROM app_notificaciones AS apn
                                WHERE apn.id_usuario = { userId }
                                ORDER BY apn.fecha_generada DESC LIMIT 15;""")
                
                resulset = cursor.fetchall()
                for row in resulset:
                    objectData = Notification(
                        int(row[0])
                        , int(row[1])
                        , (row[2]).strftime('%d/%m/%Y %H:%M:%S')
                        , (row[3]).strftime('%d/%m/%Y %H:%M:%S')
                        , row[4]
                        , int(row[5])
                        , int(row[6])
                        , row[7]
                        , row[8]
                        , int(row[9])
                        , int(row[10])
                    )

                    listObjectsNotificactions.append(objectData.to_json())
                self.CONNECTION.close()
                return listObjectsNotificactions
            
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
