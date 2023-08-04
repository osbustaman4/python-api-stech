import json
import traceback

from src.database.db_mysql import get_connection
from src.models.AppPreguntasFrecuentes import AppPreguntasFrecuentes
from src.models.CarSelect import CarSelect
from src.models.DtTracker import DtTracker
from src.models.GsUserObjects import GsUserObjects
from src.models.GsUserZones import GsUserZones
from src.models.GsUsers import GsUsers
from src.models.Notification import Notification
from src.utils.Logger import Logger

class NotificationService():

    CONNECTION = get_connection()

    @classmethod
    def loginApp(self, data):

        email = data['email']
        password = data['password']
        token = data['token']
        device = data['device']

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute("CALL wsapp_login(%s, %s, %s, %s)", (email, password, token, device))
                self.CONNECTION.commit()
                return cursor._rows
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def userUpdate(self, data):

        user = data['usuario']
        mail = data['email']
        info = json.dumps(data['info'])

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute("""
                                    UPDATE gs_users 
                                    SET info = %s
                                    WHERE id = %s AND email = %s;
                                """, (info, user, mail))
                self.CONNECTION.commit()
                return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def userSelect(self, data):

        if isinstance(data, dict):
            user = data['id_usuario']
        else:
            user = data

        try:
            listObjectsData = []
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""
                                SELECT 
                                    id,
                                    email,
                                    username,
                                    privileges,
                                    info,
                                    timezone,
                                    active
                                FROM 
                                    gs_users 
                                WHERE 
                                    id = { user };
                                """)
                resulset = cursor._rows
                for row in resulset:
                    objectData = GsUsers(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6]
                    )
                    listObjectsData.append(objectData.to_json())
                return listObjectsData
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


    @classmethod
    def questionSelect(self):

        try:
            listObjectsData = []
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""
                                SELECT * FROM app_preguntas_frecuentes
                                """)
                resulset = cursor._rows
                for row in resulset:
                    objectData = AppPreguntasFrecuentes(
                        row[0],
                        row[1],
                    )
                    listObjectsData.append(objectData.to_json())
                return listObjectsData
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def geoDelete(self, data):

        user = data['id_usuario']
        imei = data['imei']

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""
                                UPDATE gs_user_zones
                                SET 
                                    zone_visible = 'false', 
                                    zone_name_visible = 'false',
                                    zone_color = '#d50000'
                                WHERE 
                                    zone_name LIKE 'Geocerca Temporal%' 
                                    AND zone_visible ='true' 
                                    AND zone_name_visible = 'true' 
                                    AND imei = { imei } 
                                    AND user_id = { user };
                                """)
                self.CONNECTION.commit()
                return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def geoSelect(self, data):

        user = data['usuario']

        try:
            listObjectsData = []
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""
                                SELECT 
                                    gs_user_zones.zone_vertices, 
                                    gs_user_zones.imei 
                                FROM gpsimple.gs_user_zones 
                                WHERE zone_visible='true' 
                                    AND zone_name_visible='true'	
                                    AND zone_name LIKE 'Geocerca Temporal%'
                                    AND user_id = {user}
                                """)
                resulset = cursor._rows
                for row in resulset:
                    objectData = GsUserZones(
                        row[0],
                        row[1],
                    )
                    listObjectsData.append(objectData.to_json())
                return listObjectsData
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def geoInsert(self, data):

        user = data['usuario']
        imei = data['imei']
        vertices = data['vertices']
        patent = data['patente']

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute("CALL appv2_geocercas_insertar(%s, %s, %s, %s)", (user, imei, vertices, patent))
                self.CONNECTION.commit()
                return cursor._rows
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def motorCut(self, data):

        imei = data['imei']
        command = data['comando']

        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute("CALL appv2_vehiculos_corte_motor(%s, %s)", (imei, command))
                self.CONNECTION.commit()
                return cursor._rows
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def carSelect(self, data):

        user = data['id_usuario']

        try:
            listObjectsData = []
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f""" 
                                SELECT 
                                    gs_objects.name, 
                                    gs_objects.plate_number, 
                                    gs_objects.lat, 
                                    gs_objects.lng, 
                                    CONCAT(
                                        gs_objects.lat, ', ', gs_objects.lng
                                    ) as latLng, 
                                    gs_objects.speed, 
                                    gs_objects.imei, 
                                    gs_objects.angle, 
                                    gs_objects.odometer, 
                                    gs_objects.active, 
                                    gs_objects.comando_corte, 
                                    gs_objects.protocol, 
                                    gs_objects.ip, 
                                    gs_objects.port, 
                                    gs_objects.params, 
                                    if(
                                        app_alertas.velocidad IS NULL, 0, app_alertas.velocidad
                                    ) as alertas, 
                                    if(
                                        gs_objects.comando_corte IS NULL 
                                        OR trim(gs_objects.comando_corte) = '', 
                                        false, 
                                        true
                                    ) as comandos, 
                                    if(
                                        gs_objects.dt_tracker < '2011-01-01 00:00:00' 
                                        OR gs_objects.dt_tracker IS NULL, 
                                        '1111-11-11 11:11:11', 
                                        gs_objects.dt_tracker
                                    ) as lastposi, 
                                    (
                                        SELECT 
                                        gs_user_zones.zone_vertices 
                                        FROM 
                                        gpsimple.gs_user_zones 
                                        WHERE 
                                        zone_visible = 'true' 
                                        AND zone_name_visible = 'true' 
                                        AND zone_name LIKE 'Geocerca Temporal%' 
                                        AND imei = gs_objects.imei 
                                        and gs_user_zones.user_id = gs_users.id
                                    ) as geocerca_imei 
                                    FROM 
                                    gs_objects 
                                    left JOIN gs_user_objects ON gs_objects.imei = gs_user_objects.imei 
                                    left JOIN gs_users ON gs_users.id = gs_user_objects.user_id 
                                    LEFT JOIN app_alertas ON app_alertas.imei = gs_objects.imei 
                                    where 
                                    gs_objects.active = 'true' 
                                    and gs_users.id = { user }
                                """)
                resulset = cursor._rows
                for row in resulset:
                    objectData = CarSelect(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        row[10],
                        row[11],
                        row[12],
                        row[13],
                        row[14],
                        row[15],
                        row[16],
                        row[17],
                    )
                    listObjectsData.append(objectData.to_json())
                return listObjectsData

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def gsObjectDataImei(self, data):

        imei = str(data['imei'])
        dt = data['date']

        try:
            listObjectsData = []
            with self.CONNECTION.cursor() as cursor:

                cursor.execute(f"""
                                    SELECT 
                                        dt_tracker, 
                                        lat,
                                        lng,
                                        altitude,
                                        speed,
                                        angle,
                                        params 
                                    FROM 
                                        gs_object_data_{imei} 
                                    ORDER BY dt_tracker ASC;
                                """)
                resulset = cursor._rows
                for row in resulset:
                    objectData = DtTracker(
                        (row[0]).strftime('%d/%m/%Y %H:%M:%S')
                        , float(row[1])
                        , float(row[2])
                        , float(row[3])
                        , float(row[4])
                        , float(row[5])
                        , str(row[6])
                    )
                    listObjectsData.append(objectData.to_json())
                return listObjectsData

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


    @classmethod
    def gsUserOjects(self, data):
        try:

            user = data['id_usuario']
            imei = data['imei']

            listObjectsData = []
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""
                                    SELECT * 
                                    FROM gs_user_objects 
                                    WHERE user_id = {user} 
                                    AND imei = '{imei}';
                                """)
                resulset = cursor._rows
                for row in resulset:
                    objectData = GsUserObjects(
                        int(row[0])
                        , int(row[1])
                        , str(row[2]) # imei
                        , int(row[3])
                        , int(row[4])
                        , int(row[5])
                        , int(row[6])
                        , bool(row[7])
                    )
                    listObjectsData.append(objectData.to_json())
                return listObjectsData

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def uploadNotiRead(self, id):
        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(f"""
                                    UPDATE app_notificaciones 
                                    SET leida = 1, 
                                    fecha_actualizada=now() 
                                    WHERE id in ({id})
                                """)
                # Confirma los cambios en la base de datos
                self.CONNECTION.commit()
            return True

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

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
                #self.CONNECTION.close()
                return listObjectsNotificactions
            
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
