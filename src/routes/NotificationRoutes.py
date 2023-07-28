import traceback
import base64
import datetime
import io
import openpyxl
import pandas as pd

from flask import Flask, request, jsonify, Blueprint, make_response


from src.services.NotificationServices import NotificationService
from src.utils.Logger import Logger


main_notiSelec = Blueprint('main_notiSelec', __name__)

@main_notiSelec.route('/', methods=['POST'])
def notiSelec():
    try:
        data = request.get_json()

        result = NotificationService.getAllNotificationUser(data['id_usuario'])

        return jsonify({'mensaje': "notificaciones", 'detalle': result })
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify({'message': "Internal Server Error", 'success': False})
        return response, 500