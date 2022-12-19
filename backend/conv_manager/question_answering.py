# -*- coding: utf-8 -*-
"""
@author: Daniel Urcia, Daniel Arteaga
"""
import sys
import random
import json
from pathlib import Path
from datetime import datetime
from backend.database.database_connection import DatabaseConnection


# ------------------------------------------------------------------
# Funciones estáticas
# ------------------------------------------------------------------
def resource_path(relative_path):
    abs_path = r'C:/Users/user/PycharmProjects/chatbot_cursos_inictel/'
    # abs_path = r'/var/www/html/chatbot_cursos_inictel/'
    return abs_path + relative_path


def get_db_info():
    database_data = {}
    dict_words = []
    fh = open(resource_path('backend/database/db_info.txt'))
    # fh = open(resource_path('backend/database/db_info.txt'))
    for line in fh:
        words = line.rstrip().split()
        dict_words.extend(words)
    database_data['user'] = dict_words[0]
    database_data['password'] = dict_words[1]
    database_data['host'] = dict_words[2]
    database_data['database'] = dict_words[3]
    return database_data


def intent_entities_mssg(user_mssg):
    """
    Función que realizará la inferencia del mensaje de usuario enviado desde el frontend para la obtención
    de intencion y entidades
    :param None:
    :return: intent, entities
    """

    # intent_dict = {'intent': 'informacion_general'}
    intent_dict = {'intent': 'informacion_precio'}
    # intent_dict = {'intent': 'inicio_conversacion'}
    # intent_dict = {'intent': 'informacion_pago'}
    # intent_dict = {'intent': 'informacion_inscripcion'}
    # intent_dict = {'intent': 'no_responder'}
    # intent_dict = {'intent': 'respuesta_estandar'}
    # intent_dict = {'intent': 'fuera_alcance'}
    # intent_dict = {'intent': 'informacion_inscripcion'}
    # intent_dict = {'intent': 'agradecimiento'}
    # intent_dict = {'intent': 'informacion_programacion'}
    # intent_dict = {'intent': 'otros'}

    # entities_dict = {'nombre_programa': 'ESPECIALISTA CERTIFICADO EN SOPORTE TÉCNICO DE COMPUTADORAS',
    #                  'nombre_curso': 'LINUX NIVEL USUARIO'}
    # entities_dict = {'nombre_curso': 'ADOBE PREMIERE'}
    entities_dict = {'nombre_curso': 'CCTV DIGITALIZADO'}
    # ---REPROGRAMACION
    # entities_dict = {'nombre_curso': 'INSTALACIÓN Y CONFIGURACIÓN DE LINUX'}
    # entities_dict = {'nombre_curso': 'ATENCIÓN AL CLIENTE I'}
    # entities_dict = {'nombre_curso': 'FUNDAMENTOS DE TELECOMUNICACIONES'}
    # ---
    # entities_dict = {'nombre_curso': 'IMPLEMENTACIÓN PARA LAS COMUNICACIONES ÓPTICAS'}
    # entities_dict = {'nombre_curso': 'SONORIZACIÓN Y EDICIÓN DIGITAL'}
    # entities_dict = {'nombre_curso': 'COMUNICACIONES MÓVILES'}
    # entities_dict = {'nombre_curso': 'REGULACIÓN DE LAS TELECOMUNICACIONES'}
    # entities_dict = {'nombre_curso': 'INTRODUCCIÓN A LA SEGURIDAD DE LA INFORMACIÓN Y NORMAS ISO 27001 Y 27002 - ANTES 17799'}
    # entities_dict = {'nombre_programa': 'ATENCION AL CLIENTE'}
    # entities_dict = {'nombre_programa': 'PROFESIONAL EN TELECOMUNICACIONES'}
    # entities_dict = {'nombre_programa': 'DISEÑO DE DATA CENTER'}
    # entities_dict = {'nombre_programa': 'GESTION DE SEGURIDAD DE LA INFORMACION'}
    # entities_dict = {'nombre_programa': 'INGENIERIA DE COMUNICACIONES INALAMBRICAS'}
    # entities_dict = {'nombre_curso': 'INSTALACIÓN Y CONFIGURACIÓN DE LINUX', 'modalidad': 'Remoto',
    #                  'id_modulo': '2', 'nivel_curso': 'Intermedio'}
    # entities_dict = {'nombre_curso': 'ADOBE AFTER EFFECTS', 'modalidad': 'virtual',
    #                  'id_modulo': '2', 'nivel_curso': 'Intermedio'}
    # entities_dict = {'nombre_curso': 'SISTEMAS SATELITALES', 'modalidad': 'virtual',
    #                  'id_modulo': '2', 'nivel_curso': 'Avanzado'}
    # entities_dict = {'modalidad': 'Dann', 'id_modulo': '8', 'nivel_curso': 'Intermedio'}
    # entities_dict = {'nombre_programa': 'ESPECIALISTA CERTIFICADO EN SOPORTE TÉCNICO DE COMPUTADORAS'}
    # entities_dict = {'modalidad': 'Dann', 'id_modulo': '8', 'nivel_curso': 'Intermedio'}
    # entities_dict = {'nombre_programa': 'ATENCION AL CLIENTE'}
    # entities_dict = {'nombre_programa': 'ESPECIALISTA CERTIFICADO EN SOPORTE TÉCNICO DE COMPUTADORAS'}
    # entities_dict = {'nombre_programa': 'ESPECIALISTA CERTIFICADO EN SOPORTE TÉCNICO DE COMPUTADORAS', 'nombre_curso': 'LINUX NIVEL USUARIO'}
    # entities_dict = {'nombre_curso': 'SISTEMAS SATELITALES'}
    # entities_dict = {'nombre_curso': 'DISEÑO DE SISTEMAS MÓVILES CELULARES'}
    # entities_dict = {'id_modulo': '6', 'nivel_curso': 'Basico', 'modalidad': ''}
    # entities_dict = {'nombre_curso': '', 'nivel_curso': 'Intermedio'}
    # entities_dict = {}
    return intent_dict, entities_dict


def conversation_tree(db_connection, intent_dict, entities_dict, rec_received, data):
    """
    Función principal del programa
    :param intent: intención del mensaje de usuario obtenido de la inferencia de la red neuronal
    :param entities_dict: diccionario de entidades con sus respectivos values obtenidos de la inferencia
                          de la red neuronal (lo que envía el usuario). Se está tomando como intenciones principales
                          a informacion_general, infomracion_precio, informacion_pago, informacion_inscripcion,
                          informacion_programacion, continuacion.
    :param rec_received: diccionario que contiene la última intención mapeada en la conversación y sus respectivas
                         entidades, recibido desde el front-end.
    :param flag_errors:
    :return: response - respuesta de la lógica de conversación
    """

    global different_intent, flg, response, row, cost_rec, programacion_rec, estado_cur, reprog_cur
    global horario_cur, cur_en_prog, fec_programa

    # Inicializando variables
    flg = 0     # flag de respuestas
    row = ()    # fila del registro consultado
    cost_rec = []
    programacion_rec = []
    rec = {'id': ''}
    intent = list(intent_dict.values())[0]
    entities = list(entities_dict.keys())

    if data:
        rec_received = data[-1]

    if intent == 'informacion_general':
        # Intención informacion_general
        if len(entities) == 0:
            flg = 1
            response = answer_template()
            flg = 0
            return response
        else:
            if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                if 'nombre_curso' in entities:
                    flg = 2
                    record, msg1 = db_connection.get_curso(entities_dict['nombre_curso'])
                    row = record[0]
                    value = row[0]
                    response1 = answer_template()
                    flg = 0
                    if 'nombre_programa' in entities:
                        flg = 3
                        record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                        row = record[0]
                        value = row[0]
                        response2 = answer_template()
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        flg = 0
                        return response
                    return response1
                else:
                    flg = 3
                    record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                    row = record[0]
                    value = row[0]
                    response = answer_template()
                    flg = 0
                    return response
            else:
                flg = 1
                response = answer_template()
                flg = 0
                return response

    elif intent == 'informacion_precio':
        if len(entities) == 0:
            if ('nombre_curso' in rec_received) or ('nombre_programa' in rec_received):
                if 'nombre_curso' in rec_received:
                    flg = 8
                    cost_rec, msg = db_connection.get_costo_curso(rec_received['nombre_curso'])
                    response1 = answer_template()
                    flg = 0
                    if 'nombre_programa' in rec_received:
                        flg = 9
                        cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa'])
                        response2 = answer_template()
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        flg = 0
                        return response
                    return response1
                else:
                    flg = 9
                    cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa'])
                    response1 = answer_template()
                    flg = 0
                    return response1
            else:
                flg = 1
                response = answer_template()
                flg = 0
                return response
        else:
            if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                if 'nombre_curso' in entities:
                    flg = 8
                    cost_rec, msg1 = db_connection.get_costo_curso(entities_dict['nombre_curso'])
                    response1 = answer_template()
                    flg = 0
                    if 'nombre_programa' in entities:
                        flg = 9
                        cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa'])
                        response2 = answer_template()
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        flg = 0
                        return response
                    return response1
                else:
                    flg = 9
                    cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa'])
                    response = answer_template()
                    flg = 0
                    return response
            else:
                flg = 1
                response = answer_template()
                flg = 0
                return response

    elif intent == 'inicio_conversacion':
        flg = 4
        response = answer_template()
        flg = 0
        return response

    elif intent == 'agradecimiento':
        flg = 5
        response = answer_template()
        flg = 0
        return response

    elif intent == 'informacion_pago':
        flg = 6
        response = answer_template()
        flg = 0
        return response

    elif intent == 'informacion_inscripcion':
        flg = 7
        response = answer_template()
        flg = 0
        return response

    elif intent == 'informacion_programacion':
        if len(entities) == 0:
            if ('nombre_curso' in rec_received) or ('nombre_programa' in rec_received):
                if 'nombre_curso' in rec_received:
                    flg = 10
                    programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                        db_connection.get_programacion(rec_received['nombre_curso'])
                    response1 = answer_template()
                    flg = 0
                    if 'nombre_programa' in rec_received:
                        flg = 11
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(rec_received['nombre_programa'])
                        row = [nombre_curso, rec_received['nombre_programa']]
                        response2 = answer_template()
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        flg = 0
                        return response
                    return response1
                else:
                    flg = 11
                    fec_programa, nombre_curso, msg = db_connection.get_date_programa(rec_received['nombre_programa'])
                    row = [nombre_curso, rec_received['nombre_programa']]
                    response = answer_template()
                    flg = 0
                    return response
            else:
                flg = 1
                response = answer_template()
                flg = 0
                return response
        else:
            if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                if 'nombre_curso' in entities:
                    flg = 10
                    programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                        db_connection.get_programacion(entities_dict['nombre_curso'])
                    response1 = answer_template()
                    flg = 0
                    if 'nombre_programa' in entities:
                        flg = 11
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(entities_dict['nombre_programa'])
                        row = [nombre_curso, entities_dict['nombre_programa']]
                        response2 = answer_template()
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        flg = 0
                        return response
                    return response1
                else:
                    flg = 11
                    fec_programa, nombre_curso, msg = db_connection.get_date_programa(entities_dict['nombre_programa'])
                    row = [nombre_curso, entities_dict['nombre_programa']]
                    response = answer_template()
                    flg = 0
                    return response
            else:
                flg = 1
                response = answer_template()
                flg = 0
                return response

    elif intent == 'no_responder':
        flg = 12
        response = answer_template()
        flg = 0
        return response

    elif intent == 'respuesta_estandar':
        flg = 13
        response = answer_template()
        flg = 0
        return response

    elif intent == 'fuera_alcance':
        flg = 14
        response = answer_template()
        flg = 0
        return response

    elif intent == 'continuacion':
        flg = 15
        response = answer_template()
        flg = 0
        return response, row, cost_rec

    elif intent == 'otros':
        if rec_received['intent'] == 'informacion_general':
            if len(entities) == 0:
                flg = 1
                response = answer_template()
                flg = 0
                return response
            else:
                if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                    if 'nombre_curso' in entities:
                        flg = 2
                        record, msg1 = db_connection.get_curso(entities_dict['nombre_curso'])
                        row = record[0]
                        value = row[0]
                        response1 = answer_template()
                        flg = 0
                        if 'nombre_programa' in entities:
                            flg = 3
                            record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                            row = record[0]
                            value = row[0]
                            response2 = answer_template()
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            flg = 0
                            return response
                        return response1
                    else:
                        flg = 3
                        record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                        row = record[0]
                        value = row[0]
                        response = answer_template()
                        flg = 0
                        return response
                else:
                    flg = 1
                    response = answer_template()
                    flg = 0
                    return response
        elif rec_received['intent'] == 'informacion_precio':
            if len(entities) == 0:
                if ('nombre_curso' in rec_received) or ('nombre_programa' in rec_received):
                    if 'nombre_curso' in rec_received:
                        flg = 8
                        cost_rec, msg = db_connection.get_costo_curso(rec_received['nombre_curso'])
                        response1 = answer_template()
                        flg = 0
                        if 'nombre_programa' in rec_received:
                            flg = 9
                            cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa'])
                            response2 = answer_template()
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            flg = 0
                            return response
                        return response1
                    else:
                        flg = 9
                        cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa'])
                        response1 = answer_template()
                        flg = 0
                        return response1
                else:
                    flg = 1
                    response = answer_template()
                    flg = 0
                    return response
            else:
                if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                    if 'nombre_curso' in entities:
                        flg = 8
                        cost_rec, msg1 = db_connection.get_costo_curso(entities_dict['nombre_curso'])
                        response1 = answer_template()
                        flg = 0
                        if 'nombre_programa' in entities:
                            flg = 9
                            cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa'])
                            response2 = answer_template()
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            flg = 0
                            return response
                        return response1
                    else:
                        flg = 9
                        cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa'])
                        response = answer_template()
                        flg = 0
                        return response
                else:
                    flg = 1
                    response = answer_template()
                    flg = 0
                    return response
        elif rec_received['intent'] == 'informacion_programacion':
            if len(entities) == 0:
                if ('nombre_curso' in rec_received) or ('nombre_programa' in rec_received):
                    if 'nombre_curso' in rec_received:
                        flg = 10
                        programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                            db_connection.get_programacion(rec_received['nombre_curso'])
                        response1 = answer_template()
                        flg = 0
                        if 'nombre_programa' in rec_received:
                            flg = 11
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                rec_received['nombre_programa'])
                            row = [nombre_curso, rec_received['nombre_programa']]
                            response2 = answer_template()
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            flg = 0
                            return response
                        return response1
                    else:
                        flg = 11
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                            rec_received['nombre_programa'])
                        row = [nombre_curso, rec_received['nombre_programa']]
                        response = answer_template()
                        flg = 0
                        return response
                else:
                    flg = 1
                    response = answer_template()
                    flg = 0
                    return response
            else:
                if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                    if 'nombre_curso' in entities:
                        flg = 10
                        programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                            db_connection.get_programacion(entities_dict['nombre_curso'])
                        response1 = answer_template()
                        flg = 0
                        if 'nombre_programa' in entities:
                            flg = 11
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                entities_dict['nombre_programa'])
                            row = [nombre_curso, entities_dict['nombre_programa']]
                            response2 = answer_template()
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            flg = 0
                            return response
                        return response1
                    else:
                        flg = 11
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                            entities_dict['nombre_programa'])
                        row = [nombre_curso, entities_dict['nombre_programa']]
                        response = answer_template()
                        flg = 0
                        return response
                else:
                    flg = 1
                    response = answer_template()
                    flg = 0
                    return response
        else:
            # Buscando la última intención diferente a "otros" en el registro .json
            intents_chat = []
            for i in data:
                # print(i)
                intents_chat.append(i['intent'])
            # intents_chat.append(rec['intent'])
            # print('Intenciones totales de la plática', intents_chat)
            for w in range(len(intents_chat), 0, -1):
                if (intents_chat[w - 1] != 'otros') and (intents_chat[w - 1] != 'inicio_conversacion') \
                        and (intents_chat[w - 1] != 'agradecimiento'):
                    different_intent = intents_chat[w - 1]
                    # print('Reemplazar el intent de rec')
                    # rec['intent'] = last_intent_differentx
                    break
            print('different_intent: ', different_intent)

            if different_intent == 'informacion_general':
                if len(entities) == 0:
                    flg = 1
                    response = answer_template()
                    flg = 0
                    return response
                else:
                    if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                        if 'nombre_curso' in entities:
                            flg = 2
                            record, msg1 = db_connection.get_curso(entities_dict['nombre_curso'])
                            row = record[0]
                            value = row[0]
                            response1 = answer_template()
                            flg = 0
                            if 'nombre_programa' in entities:
                                flg = 3
                                record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                                row = record[0]
                                value = row[0]
                                response2 = answer_template()
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                flg = 0
                                return response
                            return response1
                        else:
                            flg = 3
                            record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                            row = record[0]
                            value = row[0]
                            response = answer_template()
                            flg = 0
                            return response
                    else:
                        flg = 1
                        response = answer_template()
                        flg = 0
                        return response
            elif different_intent == 'informacion_precio':
                if len(entities) == 0:
                    if ('nombre_curso' in rec_received) or ('nombre_programa' in rec_received):
                        if 'nombre_curso' in rec_received:
                            flg = 8
                            cost_rec, msg = db_connection.get_costo_curso(rec_received['nombre_curso'])
                            response1 = answer_template()
                            flg = 0
                            if 'nombre_programa' in rec_received:
                                flg = 9
                                cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa'])
                                response2 = answer_template()
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                flg = 0
                                return response
                            return response1
                        else:
                            flg = 9
                            cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa'])
                            response1 = answer_template()
                            flg = 0
                            return response1
                    else:
                        flg = 1
                        response = answer_template()
                        flg = 0
                        return response
                else:
                    if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                        if 'nombre_curso' in entities:
                            flg = 8
                            cost_rec, msg1 = db_connection.get_costo_curso(entities_dict['nombre_curso'])
                            response1 = answer_template()
                            flg = 0
                            if 'nombre_programa' in entities:
                                flg = 9
                                cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa'])
                                response2 = answer_template()
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                flg = 0
                                return response
                            return response1
                        else:
                            flg = 9
                            cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa'])
                            response = answer_template()
                            flg = 0
                            return response
                    else:
                        flg = 1
                        response = answer_template()
                        flg = 0
                        return response
            elif different_intent == 'informacion_programacion':
                if len(entities) == 0:
                    if ('nombre_curso' in rec_received) or ('nombre_programa' in rec_received):
                        if 'nombre_curso' in rec_received:
                            flg = 10
                            programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                                db_connection.get_programacion(rec_received['nombre_curso'])
                            response1 = answer_template()
                            flg = 0
                            if 'nombre_programa' in rec_received:
                                flg = 11
                                fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                    rec_received['nombre_programa'])
                                row = [nombre_curso, rec_received['nombre_programa']]
                                response2 = answer_template()
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                flg = 0
                                return response
                            return response1
                        else:
                            flg = 11
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                rec_received['nombre_programa'])
                            row = [nombre_curso, rec_received['nombre_programa']]
                            response = answer_template()
                            flg = 0
                            return response
                    else:
                        flg = 1
                        response = answer_template()
                        flg = 0
                        return response
                else:
                    if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                        if 'nombre_curso' in entities:
                            flg = 10
                            programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                                db_connection.get_programacion(entities_dict['nombre_curso'])
                            response1 = answer_template()
                            flg = 0
                            if 'nombre_programa' in entities:
                                flg = 11
                                fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                    entities_dict['nombre_programa'])
                                row = [nombre_curso, entities_dict['nombre_programa']]
                                response2 = answer_template()
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                flg = 0
                                return response
                            return response1
                        else:
                            flg = 11
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                entities_dict['nombre_programa'])
                            row = [nombre_curso, entities_dict['nombre_programa']]
                            response = answer_template()
                            flg = 0
                            return response
                    else:
                        flg = 1
                        response = answer_template()
                        flg = 0
                        return response
            elif different_intent == 'informacion_pago':
                flg = 6
                response = answer_template()
                flg = 0
                return response
            elif different_intent == 'informacion_inscripcion':
                flg = 7
                response = answer_template()
                flg = 0
                return response
            elif different_intent == 'no_responder':
                flg = 12
                response = answer_template()
                flg = 0
                return response
            elif different_intent == 'respuesta_estandar':
                flg = 13
                response = answer_template()
                flg = 0
                return response
            elif different_intent == 'fuera_alcance':
                flg = 14
                response = answer_template()
                flg = 0
                return response
            elif different_intent == 'continuacion':
                flg = 15
                response = answer_template()
                flg = 0
                return response, row, cost_rec


def answer_template():
    """
    Función que simula una plantilla de respuestas para cada caso del árbol de conversación.
    :param value: refiere al valor entero de la fila o registro a consultar
    :return: response
    """
    if flg == 1:
        resp = 'Genial!. ¿Podrías indicarme el nombre del curso para brindarte información?'
        return resp
    elif flg == 2:
        resp = 'El curso ' + row[1] + ' es un curso de tipo ' + row[4] + ' y se describe como: ' + row[2] + \
               '. Además, este curso posee una duración general de ' + str(row[5]) + ' horas.'
        return resp
    elif flg == 3:
        resp = 'El programa ' + row[1] + ' ' + row[2] + \
                   '. Este programa tiene una duración general de ' + str(row[4]) + ' horas.'
        return resp
    elif flg == 4:
        resp = '¡Hola! Soy la IA del INICTEL-UNI y te brindaré información con todo lo relacionado a los ' \
               'cursos y/o programas. ¿En qué te puedo ayudar?'
        return resp
    elif flg == 5:
        thanks = ['Gracias a ti', 'De nada', 'Un placer', 'Gracias por escribirme', 'Un gusto', 'Encantado de ayudarte']
        resp = random.choice(thanks)
        return resp
    elif flg == 6:
        resp = 'Los métodos de pago son dos: \n * PAGOS EN EFECTIVO se realizan directamente en ' \
                'INICTEL-UNI, en el horario de Lunes a Viernes de 08:30 hrs a 17:00 hrs. \n * DEPÓSITOS ' \
                'BANCARIOS se pueden realizar a la Cta. Cte. en soles Nº 0000-861464 del Banco de la Nación, ' \
                'debiendo ingresar \n   en los respectivos casilleros los datos del depósito ' \
                '(fecha, monto y procedencia). Una vez realizado el depósito o la \n   transferencia, ' \
                'sírvase confirmarnos por medio de fax o correo electrónico, enviando el comprobante ' \
                'de la operación al \n   correo electrónico: teleduca@inictel-uni.edu.pe, indicando el curso, ' \
                'su dirección y algún teléfono de referencia.'
        return resp
    elif flg == 7:
        resp = 'Para inscribirte debes de seguir los siguientes pasos:\n\nIngresar tus datos correctamente en el ' \
                'formulario de Pre-inscripción o enviar un correo solicitando mayores\ndetalles: ' \
                'teleduca@inictel-uni.edu.pe (*)\nLuego debes remitir los siguientes documentos ' \
                'escaneados:\n\n* Copia de su DNI, copia del Grado de Bachiller, Título o Licenciatura ' \
                'Universitaria o Certificado Técnico al\n  e-mail: teleduca@inictel-uni.edu.pe (**)\n* Fotografia ' \
                'tamaño carnet o pasaporte (**)\n* Deberá realizar el depósito (***) por el costo del curso a ' \
                'través de la Cta. Cte. en soles del Banco de la\n  Nación Nº 0000-861464.\n* Enviar la copia ' \
                'escaneada del voucher del pago realizado al e-mail: teleduca@inictel-uni.edu.pe (****)'
        return resp
    elif flg == 8:
        if len(cost_rec) == 1:
            if cost_rec[0][1] == 'L':
                resp = 'El curso ' + cost_rec[0][0] + ' tiene un ' + cost_rec[0][2] + \
                       ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                       str(cost_rec[0][4]) + ' dolares americanos.'
                return resp
            else:
                resp = 'El curso ' + cost_rec[0][0] + ' tiene un ' + cost_rec[0][2] + \
                       ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                       str(cost_rec[0][4]) + ' dolares americanos.'
                return resp
        elif len(cost_rec) == 2:
            if (cost_rec[0][1] == 'L') and (cost_rec[1][1] == 'M'):
                resp = 'El curso ' + cost_rec[0][0] + ' puede llevarse de dos formas, como curso LIBRE o ' \
                       'como parte de un MÓDULO. Su ' + cost_rec[0][2] + ' es igual a ' + \
                       str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                       str(cost_rec[0][4]) + ' dolares americanos.' 'El ' + cost_rec[1][2] + \
                       ' es igual a ' + str(cost_rec[1][3]) + ' nuevo soles, o lo que equivale a ' + \
                       str(cost_rec[1][4]) + ' dolares americanos.'
                return resp
            else:
                resp = 'El curso ' + cost_rec[0][0] + ' puede llevarse de dos formas, como curso LIBRE o ' \
                                                             'como parte de un MÓDULO. Su ' + cost_rec[1][
                           2] + ' es igual a ' + \
                       str(cost_rec[1][3]) + ' nuevo soles, o lo que equivale a ' + \
                       str(cost_rec[1][4]) + ' dolares americanos y su ' + cost_rec[0][2] + \
                       ' es igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                       str(cost_rec[0][4]) + ' dolares americanos.'
                return resp
        else:
            resp = '¡Lo siento! Por el momento, no dispongo de información sobre los precios de este curso.'
            return resp
    elif flg == 9:
        if cost_rec[0][1] == 'COSTO TOTAL DEL PROGRAMA':
            resp = 'El programa ' + cost_rec[0][0] + ' tiene un costo total de ' + str(cost_rec[0][2]) + \
                   ' nuevos soles, o lo que equivale a ' + str(cost_rec[0][3]) + ' dolares americanos. Además, ' \
                   'tiene un costo de matrícula igual a ' + str(cost_rec[1][2]) + ' nuevo soles, o ' + \
                   str(cost_rec[1][3]) + ' dolares americanos.'
            return resp
        else:
            resp = 'El programa ' + cost_rec[1][0] + ' tiene un costo total de ' + str(cost_rec[1][2]) + \
                   ' nuevos soles, o lo que equivale a ' + str(cost_rec[1][3]) + ' dolares americanos. Además, ' \
                   'tiene un costo de matrícula igual a ' + str(cost_rec[0][2]) + ' nuevo soles, o ' + \
                   str(cost_rec[0][3]) + ' dolares americanos.'
            return resp
    elif flg == 10:
        # Fechas de programación del curso
        f1 = programacion_rec[0][2]
        f2 = programacion_rec[0][3]

        # Casos según el estado del curso
        if programacion_rec[0][4] == 1:
            resp = 'El curso ' + programacion_rec[0][12] + ' pertenece al programa ' + cur_en_prog[0][1] + \
                   ', actualmente se encuentra en la condición de ' + estado_cur[0][1] + \
                   ' teniendo como fecha de inicio el ' + f1.strftime("%d-%m-%y") + \
                   ' y fecha prevista de culminación el ' + f2.strftime("%d-%m-%y") + '. Además, tiene una duración de ' + str(programacion_rec[0][16]) + \
                   ' horas calendarias y su horario corresponde a ' + horario_cur[0][1] + ' de ' + horario_cur[0][2] + \
                   ' a ' + horario_cur[0][3] + ' horas.'
            return resp
        elif programacion_rec[0][4] == 2:
            resp = 'El curso ' + programacion_rec[0][12] + ' pertenece al programa ' + cur_en_prog[0][1] + \
                   ', actualmente se encuentra ' + estado_cur[0][1] + \
                   '. Tendrá una duración de ' + str(programacion_rec[0][16]) + ' horas calendarias. Se inició el ' + \
                   f1.strftime("%d-%m-%y") + ' y culminará el ' + f2.strftime("%d-%m-%y") + '.'
            return resp
        elif programacion_rec[0][4] == 3:
            resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se encuentra ' + estado_cur[0][1] + \
                   ' y no tiene nuevas fechas programadas.'
            return resp
        elif programacion_rec[0][4] == 4:
            resp = 'El curso ' + programacion_rec[0][12] + ' se encuentra ' + estado_cur[0][1] + \
                   ' y no se está dictando en la institución.'
            return resp
        elif programacion_rec[0][4] == 5:
            resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se encuentra ' + estado_cur[0][1] + '.'
            return resp
        elif programacion_rec[0][4] == 6:
            try:
                resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se ha ' + estado_cur[0][1] + \
                        '.' + ' Tendrá una duración de ' + str(programacion_rec[0][16]) + \
                        ' horas calendarias. La nueva fecha de inicio será el ' + reprog_cur[0][0].strftime("%d-%m-%y") + \
                        ' y culminará el ' + reprog_cur[0][1].strftime("%d-%m-%y") + '.'
                return resp
            finally:
                pass
        elif programacion_rec[0][4] == 7:
            resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se encuentra ' + estado_cur[0][1] + \
                   ' y por el momento no se está dictando en la institución.'
            return resp
    elif flg == 11:
        # Se responde con la fecha de programación del 1er curso (modulo) del programa
        resp = 'El programa ' + row[1] + ' inicia el ' \
               + fec_programa[0][2].strftime("%d-%m-%y") + ' con el primer módulo ' \
               + row[0]
        return resp
    elif flg == 12:
        # Estas son las respuestas de la intención "otros"
        response = 'Respuesta de flg=12'
        return response
    elif flg == 13:
        resp_estandar = ['Ok', 'Bien', 'Genial', 'Excelente', 'Está bien', 'Vale']
        response = random.choice(resp_estandar)
        return response
    elif flg == 14:
        response = 'No logro comprenderte. ¿Podrías escribir nuevamente tu consulta?'
        return response
    elif flg == 15:
        response = 'Esta es la intencion continuacion'
        return response


if __name__ == "__main__":
    connect_params = get_db_info()
    db_connection = DatabaseConnection(connect_params)
    # user_id = int(sys.argv[1])
    # user_name = sys.argv[2]
    # user_msg = sys.argv[3]
    user_name = 'jp'
    user_mssg = ['']
    register = []
    path = Path(resource_path('conversations/register_' + user_name + '.json'))
    if path.is_file():
        # Abriendo el archivo JSON para acceder al id
        json_file = open(resource_path('conversations/register_' + user_name + '.json'))
        json_data = json.load(json_file)
        # Agregando el nuevo rec al json
        rec_received = json_data[len(json_data) - 1]
        print('rec_received: ', rec_received)
        intent_dict, entities_dict = intent_entities_mssg(user_mssg)
        rec = dict()
        rec['id'] = len(json_data) + 1
        rec['intent'] = intent_dict['intent']
        for key, value in entities_dict.items():
            rec[key] = value
        response_final = conversation_tree(db_connection, intent_dict, entities_dict, 'rec_received', json_data)
        with open(resource_path('conversations/register_' + user_name + '.json'), "r+", encoding='utf-8') as file:
            data = json.load(file)
            data.append(rec)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        # Crear el json y guardar el rec
        rec_received = {}
        print('rec_received: ', rec_received)
        intent_dict, entities_dict = intent_entities_mssg([])
        rec = dict()
        rec['id'] = 1
        rec['intent'] = intent_dict['intent']
        for key, value in entities_dict.items():
            rec[key] = value
        register.append(rec)
        with open(resource_path('conversations/register_' + user_name + '.json'), 'w', encoding='utf-8') as file:
            json.dump(register, file, indent=4)
        response_final = conversation_tree(db_connection, intent_dict, entities_dict, rec_received, [])

    # db_cost_query('costo_curso', 'cod_curso', 7)
    print('response: ', response_final)
    print('rec: ', rec)
