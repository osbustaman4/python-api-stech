import traceback
import base64
import datetime
import io
import openpyxl
import pandas as pd

from flask import Flask, request, jsonify, Blueprint, make_response
from src.decorators.AuthToken import verify_token

from src.services.ObjectDataServices import ObjectDataService
from src.utils.Logger import Logger

main_get_data = Blueprint('main_get_data', __name__)
main_getObjectData = Blueprint('main_getObjectData', __name__)
main_getObjectDataJson = Blueprint('main_getObjectDataJson', __name__)

@main_get_data.route('/')
def get_data():
    try:
        return "Ok - se levanta app en Flask"
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify({'message': "Internal Server Error", 'success': False})
        return response, 500

@main_getObjectDataJson.route('/')
def getObjectDataJson():
    try:
        data = ObjectDataService.get_data()

        return jsonify({'success': True, 'response': data})
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify({'message': "Internal Server Error", 'success': False})
        return response, 500

@main_getObjectData.route('/')
def getObjectData():
    try:
        data = ObjectDataService.get_data()

        # se crean las cabeceras
        head_data = ['dt_server', 'dt_tracket', 'latitud', 'longitud', 'altitud', 'angulo', 'velocidad', 'parametros']


        # Crea un DataFrame vacío para cada hoja del Excel
        df_data = pd.DataFrame(columns=head_data)


        filename_excel ='plantilla_carga_masiva.xlsx'
        writer = pd.ExcelWriter(f'{filename_excel}', engine='xlsxwriter')


        # Escribe cada DataFrame en una hoja del archivo Excel
        df_data.to_excel(writer, sheet_name='datos frame', index=False)


        # Asigna las cabeceras a cada DataFrame
        df_data.columns = head_data


        # Guarda el archivo Excel
        writer.close()


        # Abre el archivo Excel existente
        workbook = openpyxl.load_workbook(filename=filename_excel)

        sheetData = workbook['datos frame']

        cont = 2
        for element in data:
            sheetData[f'A{cont}'] = element['dt_server']
            sheetData[f'B{cont}'] = element['dt_tracker']
            sheetData[f'C{cont}'] = element['lat']
            sheetData[f'D{cont}'] = element['lng']
            sheetData[f'E{cont}'] = element['altitude']
            sheetData[f'F{cont}'] = element['angle']
            sheetData[f'G{cont}'] = element['speed']
            sheetData[f'H{cont}'] = element['params']
            cont += 1

        workbook.save(filename_excel)


        # Codifica el archivo en base64
        with open(filename_excel, 'rb') as file:
            base64_encoded_file = base64.b64encode(file.read()).decode('utf-8').replace('\n', '')

        
        # Establece el tipo de contenido como 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = make_response(base64_encoded_file)
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = 'attachment; filename=plantilla_carga_masiva.xlsx'

        
        return jsonify({'success': True, 'base64_encoded_file': base64_encoded_file})

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify({'message': "Internal Server Error", 'success': False})
        return response, 500