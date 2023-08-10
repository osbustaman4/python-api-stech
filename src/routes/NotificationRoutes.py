import json
import traceback

from flask import request, jsonify, Blueprint
from src.models.error.HTTP404Error import HTTP404Error

from src.services.NotificationServices import NotificationService
from src.utils.Logger import Logger

main_notiSelec = Blueprint('main_notiSelec', __name__)
main_notiRead = Blueprint('main_notiRead', __name__)
main_carHistory = Blueprint('main_carHistory', __name__)
main_carSelect = Blueprint('main_carSelect', __name__)
main_motorCut = Blueprint('main_motorCut', __name__)
main_geoInsert = Blueprint('main_geoInsert', __name__)
main_geoSelect = Blueprint('main_geoSelect', __name__)
main_geoDelete = Blueprint('main_geoDelete', __name__)
main_questionSelect = Blueprint('main_questionSelect', __name__)
main_userSelect = Blueprint('main_userSelect', __name__)
main_userUpdate = Blueprint('main_userUpdate', __name__)
main_loginApp = Blueprint('main_loginApp', __name__)

@main_loginApp.route('/', methods=['POST'])
def loginApp():
    try:
        data = request.get_json()
        objects = NotificationService.loginApp(data)

        if not objects:
            raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
        else:
            if "exito" in objects[0][0]:
                infoUser = NotificationService.userSelect(int((objects[0][0]).split(" ")[1]))[0]

                if infoUser:
                    response = {
                        "id": infoUser['id'],
                        "email": infoUser['email'],
                        "username": infoUser['username'],
                        "tipo_user": json.loads(infoUser['tipo_user'])['type'],
                        "info": json.loads(infoUser['info']),
                        "timezone": infoUser['timezone'],
                        "activo": infoUser['activo']
                    }
                    return jsonify(response)
                else:
                    raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
            else:
                raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
            
    except HTTP404Error as ex:
        response = jsonify(
            {'message': f"{ str(ex) }", 'success': False})
        return response, 404

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500


@main_userUpdate.route('/', methods=['POST'])
def userUpdate():
    try:
        data = request.get_json()
        objects = NotificationService.userUpdate(data)

        if not objects:
            raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
        else:
            response = {
                    "mensaje": "información actualizada",
                    "success": True
            }
            return jsonify(response)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500


@main_userSelect.route('/', methods=['POST'])
def userSelect():
    try:
        data = request.get_json()
        objects = NotificationService.userSelect(data)

        if not objects:
            raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
        else:
            infoUser = objects[0]
            response = {
                    "id": infoUser['id'],
                    "email": infoUser['email'],
                    "username": infoUser['username'],
                    "tipo_user": json.loads(infoUser['tipo_user'])['type'],
                    "info": json.loads(infoUser['info']),
                    "timezone": infoUser['timezone'],
                    "activo": infoUser['activo']
                }
            return jsonify(response)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500

@main_questionSelect.route('/', methods=['GET'])
def questionSelect():
    try:
        objects = NotificationService.questionSelect()

        if not objects:
            raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
        else:
            response = {
                    "mensaje": "FAQ",
                    "detalle": objects,
                    "success": True
                }
            return jsonify(response)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500

@main_geoDelete.route('/', methods=['POST'])
def questionSelect():
    try:
        data = request.get_json()
        objects = NotificationService.geoDelete(data)

        if not objects:
            raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
        else:
            response = {
                    "mensaje": "Geocerca Eliminada"
                }
            return jsonify(response)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500

@main_geoSelect.route('/', methods=['POST'])
def geoSelect():
    try:
        data = request.get_json()
        objects = NotificationService.geoSelect(data)

        if not objects:
            raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
        else:

            geoJson = []
            for obj in objects:
                geoJson.append({
                    "imei": obj["imei"],
                    "lat": str((obj["zone_vertices"]).split(",")[0]),
                    "lng": str((obj["zone_vertices"]).split(",")[1])
                })

            response = {
                    "mensaje": f"Geocercas de Usuario",
                    "detalle": geoJson,
                    "success": True
                }
            return jsonify(response)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500


@main_geoInsert.route('/', methods=['POST'])
def geoInsert():
    try:
        data = request.get_json()
        objects = NotificationService.geoInsert(data)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500

@main_motorCut.route('/', methods=['POST'])
def motorCut():
    try:
        data = request.get_json()
        objects = NotificationService.motorCut(data)
        
        if objects[0][0] == "error":
            raise HTTP404Error("HTTP 404 - No se encontro dato para mostrar")
        else:
            response = {
                    "mensaje": f"exito para sp",
                    "detalle": objects[0][0],
                    "success": True
                }
            return jsonify(response)
        
    except HTTP404Error as ex:
        response = jsonify(
            {'message': f"{ str(ex) }", 'success': False})
        return response, 404

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500

@main_carSelect.route('/', methods=['POST'])
def carSelect():
    try:
        data = request.get_json()
        objects = NotificationService.carSelect(data)

        if objects:
            response = {
                "mensaje": f"{ len(objects) } Vehículos Encontrados",
                "dispos": objects
            }
            return jsonify(response)
        else:
            raise HTTP404Error()
    
    except HTTP404Error as ex:
        response = jsonify(
            {'message': f"error: { str(ex) }", 'success': False})
        return response, 404

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500

@main_carHistory.route('/', methods=['POST'])
def carHistory():
    try:
        data = request.get_json()
        queryProp = NotificationService.gsUserOjects(data)

        if not queryProp:
            raise HTTP404Error()
        else:

            dataToConsult = {
                "imei": queryProp[0]['imei'],
                "date": data['fecha'],
            }

            queryhist = NotificationService.gsObjectDataImei(dataToConsult)
            return jsonify({'mensaje': f"historial para día: {data['fecha']}", 'detalle': queryhist})
    except HTTP404Error as ex:
        response = jsonify(
            {'message': f"El vehículo con IMEI '{ data['imei'] }' no está asociado al usuario con ID '{ data['id_usuario'] }'.", 'success': False})
        return response, 404

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500


@main_notiSelec.route('/', methods=['POST'])
def notiSelec():
    try:
        data = request.get_json()
        result = NotificationService.getAllNotificationUser(data['id_usuario'])
        return jsonify({'mensaje': "notificaciones", 'detalle': result})
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify(
            {'message': "Internal Server Error", 'success': False})
        return response, 500


@main_notiRead.route('/', methods=['POST'])
def notiRead():
    try:
        data = request.get_json()
        NotificationService.uploadNotiRead(data['id_usuario'])
        return jsonify({'mensaje': "Notificaciones marcadas como leidas"})
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify({'message': "Internal Server Error",
                            'success': False, "error": str(ex)})
        return response, 500
