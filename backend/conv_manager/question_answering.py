# -*- coding: utf-8 -*-
"""
@author: Daniel Urcia, Daniel Arteaga
"""
import os
import sys
import random
import json
from pathlib import Path
from datetime import datetime
from backend.database.database_connection import DatabaseConnection
from backend.nlu.inference import nlu_pipeline
import re
from dotenv import load_dotenv


load_dotenv()

CHATBOT_HOME = os.getenv('CHATBOT_HOME')

# ------------------------------------------------------------------
# Funciones estáticas
# ------------------------------------------------------------------
def resource_path(relative_path):
    abs_path = CHATBOT_HOME
    # abs_path = r'C:/Users/darteaga/PycharmProjects/chatbot_cursos_inictel/'
    # abs_path = r'C:/Users/user/PycharmProjects/chatbot_cursos_inictel/'
    # abs_path = r'/var/www/html/chatbot_cursos_inictel/'
    return abs_path + relative_path


def get_db_info():
    database_data = {}
    dict_words = []
    fh = open(resource_path('backend/database/db_info.txt'))
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
    output_nlu = nlu_pipeline(user_mssg)
    # intent_dict = {'intent': 'informacion_general'}
    intent_dict = output_nlu["intent"]

    #intent_dict = {'intent': 'informacion_precio'}
    # intent_dict = {'intent': 'inicio_conversacion'}
    # intent_dict = {'intent': 'informacion_pago'}
    # intent_dict = {'intent': 'informacion_inscripcion'}
    # intent_dict = {'intent': 'no_responder'}
    # intent_dict = {'intent': 'respuesta_estandar'}
    # intent_dict = {'intent': 'fuera_alcance'}
    # intent_dict = {'intent': 'informacion_inscripcion'}
    # intent_dict = {'intent': 'agradecimiento'}
    # intent_dict = {'intent': 'informacion_programacion'}
    # intent_dict = {'intent': 'otra'}

    # entities_dict = {'nombre_programa': 'ESPECIALISTA CERTIFICADO EN SOPORTE TÉCNICO DE COMPUTADORAS',
    #                  'nombre_curso': 'LINUX NIVEL USUARIO'}
    # entities_dict = {'nombre_curso': 'ADOBE PREMIERE'}
    entities_dict = dict()
    #entities_dict = {'nombre_curso': 'CCTV DIGITALIZADO'}
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

    # if output_nlu['entities']:
    #     keys = []
    #     for d in output_nlu['entities']:
    #         if d['entity'] not in keys:
    #             keys.append(d['entity'])
    #             entities_dict[d['entity'].lower()] = []
    #     for d in output_nlu['entities']:
    #         value = re.sub(r'(\w)( - )(\w)', r'\1-\3', d['value'])
    #         entities_dict[d['entity'].lower()].append(value)

    if output_nlu['entities']:
        for d in output_nlu['entities']:
            value = re.sub(r'(\w)( - )(\w)', r'\1-\3', d['value'])
            entities_dict[d['entity'].lower()] = value

    return intent_dict, entities_dict


def conversation_tree(db_connection, intent_dict, entities_dict, data):
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
    global horario_cur, cur_en_prog, fec_programa, msg1, msg2

    # Inicializando variables
    flg = 0     # flag de respuestas
    row = ()    # fila del registro consultado
    cost_rec = []
    programacion_rec = []
    intent = list(intent_dict.values())[0]
    entities = list(entities_dict.keys())

    if data:
        rec_received = data[-1]
    else:
        rec_received = {}

    if intent == 'informacion_general':
        # Intención informacion_general
        if len(entities) == 0:
            response = answer_template(1)
            return response
        else:
            if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                if 'nombre_curso' in entities:
                    record, msg1 = db_connection.get_curso(entities_dict['nombre_curso'])
                    if record:
                        row = record[0]
                        value = row[0]
                    else:
                        return msg1
                    response1 = answer_template(2)
                    if 'nombre_programa' in entities:
                        record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                        if record:
                            row = record[0]
                            value = row[0]
                        else:
                            return msg2
                        response2 = answer_template(3)
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        return response
                    return response1
                else:
                    record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                    if record:
                        row = record[0]
                        value = row[0]
                    else:
                        return msg2
                    response = answer_template(3)
                    return response
            else:
                response = answer_template(1)
                return response

    elif intent == 'informacion_precio':
        if len(entities) == 0:
            if ('nombre_curso_match' in rec_received.keys()) or ('nombre_programa_match' in rec_received.keys()):
                if 'nombre_curso_match' in rec_received.keys():
                    cost_rec, msg = db_connection.get_costo_curso(rec_received['nombre_curso_match'])
                    response1 = answer_template(8)
                    if 'nombre_programa_match' in rec_received.keys():
                        cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa_match'])
                        response2 = answer_template(9)
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        return response
                    return response1
                else:
                    cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa_match'])
                    response1 = answer_template(9)
                    return response1
            else:
                response = answer_template(1)
                return response
        else:
            if ('nombre_curso_match' in entities) or ('nombre_programa_match' in entities):
                if 'nombre_curso_match' in entities:
                    cost_rec, msg1 = db_connection.get_costo_curso(entities_dict['nombre_curso_match'])
                    response1 = answer_template(8)
                    if 'nombre_programa_match' in entities:
                        cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa_match'])
                        response2 = answer_template(9)
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        return response
                    return response1
                else:
                    cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa_match'])
                    response = answer_template(9)
                    return response
            else:
                response = answer_template(14)
                return response

    elif intent == 'inicio_conversacion':
        response = answer_template(4)
        return response

    elif intent == 'agradecimiento':
        response = answer_template(5)
        return response

    elif intent == 'informacion_pago':
        response = answer_template(6)
        return response

    elif intent == 'informacion_inscripcion':
        response = answer_template(7)
        return response

    elif intent == 'informacion_programacion':
        if len(entities) == 0:
            if ('nombre_curso_match' in rec_received) or ('nombre_programa_match' in rec_received):
                if 'nombre_curso_match' in rec_received:
                    programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                        db_connection.get_programacion(rec_received['nombre_curso_match'])
                    response1 = answer_template(10)
                    if 'nombre_programa_match' in rec_received:
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                            rec_received['nombre_programa_match'])
                        row = [nombre_curso, rec_received['nombre_programa_match']]
                        response2 = answer_template(11)
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        return response
                    return response1
                else:
                    fec_programa, nombre_curso, msg = db_connection.get_date_programa(rec_received['nombre_programa_match'])
                    row = [nombre_curso, rec_received['nombre_programa_match']]
                    response = answer_template(11)
                    return response
            else:
                response = answer_template(1)
                return response
        else:
            if ('nombre_curso_match' in entities) or ('nombre_programa_match' in entities):
                if 'nombre_curso_match' in entities:
                    programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                        db_connection.get_programacion(entities_dict['nombre_curso_match'])
                    response1 = answer_template(10)
                    if 'nombre_programa_match' in entities:
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                            entities_dict['nombre_programa_match'])
                        row = [nombre_curso, entities_dict['nombre_programa_match']]
                        response2 = answer_template(11)
                        response = response1 + ' Respecto a tu segunda consulta, ' + response2
                        return response
                    return response1
                else:
                    fec_programa, nombre_curso, msg = db_connection.get_date_programa(entities_dict['nombre_programa_match'])
                    row = [nombre_curso, entities_dict['nombre_programa_match']]
                    response = answer_template(11)
                    return response
            else:
                response = answer_template(14)
                return response

    elif intent == 'no_responder':
        response = answer_template(12)
        return response

    elif intent == 'respuesta_estandar':
        response = answer_template(13)
        return response

    elif intent == 'fuera_alcance':
        response = answer_template(14)
        return response

    elif intent == 'continuacion':
        response = answer_template(15)
        return response

    elif intent == 'otra':
        if rec_received['intent'] == 'informacion_general':
            if len(entities) == 0:
                response = answer_template(1)
                return response
            else:
                if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                    if 'nombre_curso' in entities:
                        record, msg1 = db_connection.get_curso(entities_dict['nombre_curso'])
                        if record:
                            row = record[0]
                            value = row[0]
                        else:
                            return msg1
                        response1 = answer_template(2)
                        if 'nombre_programa' in entities:
                            record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                            if record:
                                row = record[0]
                                value = row[0]
                            else:
                                return msg2
                            response2 = answer_template(3)
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            return response
                        return response1
                    else:
                        record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                        if record:
                            row = record[0]
                            value = row[0]
                        else:
                            return msg2
                        response = answer_template(3)
                        return response
                else:
                    response = answer_template(1)
                    return response
        elif rec_received['intent'] == 'informacion_precio':
            if len(entities) == 0:
                if ('nombre_curso_match' in rec_received) or ('nombre_programa_match' in rec_received):
                    if 'nombre_curso_match' in rec_received:
                        cost_rec, msg = db_connection.get_costo_curso(rec_received['nombre_curso_match'])
                        response1 = answer_template(8)
                        if 'nombre_programa_match' in rec_received:
                            cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa_match'])
                            response2 = answer_template(9)
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            return response
                        return response1
                    else:
                        cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa_match'])
                        response1 = answer_template(9)
                        return response1
                else:
                    response = answer_template(1)
                    return response
            else:
                if ('nombre_curso_match' in entities) or ('nombre_programa_match' in entities):
                    if 'nombre_curso_match' in entities:
                        cost_rec, msg1 = db_connection.get_costo_curso(entities_dict['nombre_curso_match'])
                        response1 = answer_template(8)
                        if 'nombre_programa_match' in entities:
                            cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa_match'])
                            response2 = answer_template(9)
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            return response
                        return response1
                    else:
                        cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa_match'])
                        response = answer_template(9)
                        return response
                else:
                    response = answer_template(14)
                    return response
        elif rec_received['intent'] == 'informacion_programacion':
            if len(entities) == 0:
                if ('nombre_curso_match' in rec_received) or ('nombre_programa_match' in rec_received):
                    if 'nombre_curso_match' in rec_received:
                        programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                            db_connection.get_programacion(rec_received['nombre_curso_match'])
                        response1 = answer_template(10)
                        if 'nombre_programa_match' in rec_received:
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                rec_received['nombre_programa_match'])
                            row = [nombre_curso, rec_received['nombre_programa_match']]
                            response2 = answer_template(11)
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            return response
                        return response1
                    else:
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                            rec_received['nombre_programa_match'])
                        row = [nombre_curso, rec_received['nombre_programa_match']]
                        response = answer_template(11)
                        return response
                else:
                    response = answer_template(1)
                    return response
            else:
                if ('nombre_curso_match' in entities) or ('nombre_programa_match' in entities):
                    if 'nombre_curso_match' in entities:
                        programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                            db_connection.get_programacion(entities_dict['nombre_curso_match'])
                        response1 = answer_template(10)
                        if 'nombre_programa_match' in entities:
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                entities_dict['nombre_programa_match'])
                            row = [nombre_curso, entities_dict['nombre_programa_match']]
                            response2 = answer_template(11)
                            response = response1 + ' Respecto a tu segunda consulta, ' + response2
                            return response
                        return response1
                    else:
                        fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                            entities_dict['nombre_programa_match'])
                        row = [nombre_curso, entities_dict['nombre_programa_match']]
                        response = answer_template(11)
                        return response
                else:
                    response = answer_template(14)
                    return response
        else:
            # Buscando la última intención diferente a "otra" en el registro .json
            intents_chat = []
            for i in data:
                intents_chat.append(i['intent'])
            # intents_chat.append(rec['intent'])
            for w in range(len(intents_chat), 0, -1):
                if (intents_chat[w - 1] != 'otra') and (intents_chat[w - 1] != 'inicio_conversacion') \
                        and (intents_chat[w - 1] != 'agradecimiento'):
                    different_intent = intents_chat[w - 1]
                    # rec['intent'] = last_intent_differentx
                    break

            if different_intent == 'informacion_general':
                if len(entities) == 0:
                    response = answer_template(1)
                    return response
                else:
                    if ('nombre_curso' in entities) or ('nombre_programa' in entities):
                        if 'nombre_curso' in entities:
                            record, msg1 = db_connection.get_curso(entities_dict['nombre_curso'])
                            if record:
                                row = record[0]
                                value = row[0]
                            else:
                                return msg1
                            response1 = answer_template(2)
                            if 'nombre_programa' in entities:
                                record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                                if record:
                                    row = record[0]
                                    value = row[0]
                                else:
                                    return msg2
                                response2 = answer_template(3)
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                return response
                            return response1
                        else:
                            record, msg2 = db_connection.get_programa(entities_dict['nombre_programa'])
                            if record:
                                row = record[0]
                                value = row[0]
                            else:
                                return msg2
                            response = answer_template(3)
                            return response
                    else:
                        response = answer_template(1)
                        return response
            elif different_intent == 'informacion_precio':
                if len(entities) == 0:
                    if ('nombre_curso_match' in rec_received) or ('nombre_programa_match' in rec_received):
                        if 'nombre_curso_match' in rec_received:
                            cost_rec, msg = db_connection.get_costo_curso(rec_received['nombre_curso_match'])
                            response1 = answer_template(8)
                            if 'nombre_programa_match' in rec_received:
                                cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa_match'])
                                response2 = answer_template(9)
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                return response
                            return response1
                        else:
                            cost_rec, msg = db_connection.get_costo_programa(rec_received['nombre_programa_match'])
                            response1 = answer_template(9)
                            return response1
                    else:
                        response = answer_template(1)
                        return response
                else:
                    if ('nombre_curso_match' in entities) or ('nombre_programa_match' in entities):
                        if 'nombre_curso_match' in entities:
                            cost_rec, msg1 = db_connection.get_costo_curso(entities_dict['nombre_curso_match'])
                            response1 = answer_template(8)
                            if 'nombre_programa_match' in entities:
                                cost_rec, msg2 = db_connection.get_costo_programa(
                                    entities_dict['nombre_programa_match'])
                                response2 = answer_template(9)
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                return response
                            return response1
                        else:
                            cost_rec, msg2 = db_connection.get_costo_programa(entities_dict['nombre_programa_match'])
                            response = answer_template(9)
                            return response
                    else:
                        response = answer_template(14)
                        return response
            elif different_intent == 'informacion_programacion':
                if len(entities) == 0:
                    if ('nombre_curso_match' in rec_received) or ('nombre_programa_match' in rec_received):
                        if 'nombre_curso_match' in rec_received:
                            programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                                db_connection.get_programacion(rec_received['nombre_curso_match'])
                            response1 = answer_template(10)
                            if 'nombre_programa_match' in rec_received:
                                fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                    rec_received['nombre_programa_match'])
                                row = [nombre_curso, rec_received['nombre_programa_match']]
                                response2 = answer_template(11)
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                return response
                            return response1
                        else:
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                rec_received['nombre_programa_match'])
                            row = [nombre_curso, rec_received['nombre_programa_match']]
                            response = answer_template(11)
                            return response
                    else:
                        response = answer_template(1)
                        return response
                else:
                    if ('nombre_curso_match' in entities) or ('nombre_programa_match' in entities):
                        if 'nombre_curso_match' in entities:
                            programacion_rec, estado_cur, reprog_cur, horario_cur, cur_en_prog = \
                                db_connection.get_programacion(entities_dict['nombre_curso_match'])
                            response1 = answer_template(10)
                            if 'nombre_programa_match' in entities:
                                fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                    entities_dict['nombre_programa_match'])
                                row = [nombre_curso, entities_dict['nombre_programa_match']]
                                response2 = answer_template(11)
                                response = response1 + ' Respecto a tu segunda consulta, ' + response2
                                return response
                            return response1
                        else:
                            fec_programa, nombre_curso, msg = db_connection.get_date_programa(
                                entities_dict['nombre_programa_match'])
                            row = [nombre_curso, entities_dict['nombre_programa_match']]
                            response = answer_template(11)
                            return response
                    else:
                        response = answer_template(14)
                        return response
            elif different_intent == 'informacion_pago':
                response = answer_template(6)
                return response
            elif different_intent == 'informacion_inscripcion':
                response = answer_template(7)
                return response
            elif different_intent == 'no_responder':
                response = answer_template(12)
                return response
            elif different_intent == 'respuesta_estandar':
                response = answer_template(13)
                return response
            elif different_intent == 'fuera_alcance':
                response = answer_template(14)
                return response
            elif different_intent == 'continuacion':
                response = answer_template(15)
                return response


def answer_template(flg):
    """
    Función que simula una plantilla de respuestas para cada caso del árbol de conversación.
    :param value: refiere al valor entero de la fila o registro a consultar
    :return: response
    """
    global resp_match
    if flg == 1:
        resp = 'Genial!. ¿Podrías indicarme el nombre del curso para brindarte información?'
        flg = 0
        return resp
    elif flg == 2:
        if msg1 == 'dist_cero':
            resp = 'El curso ' + row[1] + ' es de tipo ' + row[4] + ' y se describe ' \
                    'como: ' + row[2] + '. Además, este curso posee una duración general de ' + str(row[5]) + ' horas.'
        else:
            resp = 'Quizá te referías al curso ' + row[1] + '. Este es un curso de tipo ' + row[4] + ' y se describe ' \
                    'como: ' + row[2] + '. Además, este curso posee una duración general de ' + str(row[5]) + ' horas.'
        flg = 0
        return resp
    elif flg == 3:
        if msg2 == 'dist_cero':
            resp = 'El programa ' + row[1] + ' ' + row[2] + \
                   '. Este programa tiene una duración general de ' + str(row[4]) + ' horas.'
        else:
            resp = 'Quizá te referías al programa ' + row[1] + '. Este programa ' + row[2] + \
                   '. Además, tiene una duración general de ' + str(row[4]) + ' horas.'
        flg = 0
        return resp
    elif flg == 4:
        resp = '¡Hola! Soy la IA del INICTEL-UNI y te brindaré información con todo lo relacionado a los ' \
               'cursos y/o programas. ¿En qué te puedo ayudar?'
        flg = 0
        return resp
    elif flg == 5:
        thanks = ['Gracias a ti', 'De nada', 'Un placer', 'Gracias por escribirme', 'Un gusto', 'Encantado de ayudarte']
        resp = random.choice(thanks)
        flg = 0
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
        flg = 0
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
        flg = 0
        return resp
    elif flg == 8:
        if cost_rec:
            if len(cost_rec) == 1:
                if cost_rec[0][1] == 'L':
                    if 'nombre_curso_match' in entities_dict.keys():
                        if entities_dict['nombre_curso_match'] != entities_dict['nombre_curso'].lower():
                            resp = 'Quizá te referías al curso de ' + cost_rec[0][0] + '. Este tiene un ' + cost_rec[0][2] + \
                                   ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[0][4]) + ' dolares americanos.'
                            flg = 0
                            return resp
                        else:
                            resp = 'El curso ' + cost_rec[0][0] + ' tiene un ' + cost_rec[0][
                                2] + \
                                   ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[0][4]) + ' dolares americanos.'
                            flg = 0
                            return resp
                    else:
                        resp = 'El curso ' + cost_rec[0][0] + ' tiene un ' + cost_rec[0][
                            2] + \
                               ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                               str(cost_rec[0][4]) + ' dolares americanos.'
                        flg = 0
                        return resp
                else:
                    if 'nombre_curso_match' in entities_dict.keys():
                        if entities_dict['nombre_curso_match'] != entities_dict['nombre_curso'].lower():
                            resp = 'Quizá te referías al curso de ' + cost_rec[0][0] + '. Este tiene un ' + cost_rec[0][2] + \
                                   ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[0][4]) + ' dolares americanos.'
                            flg = 0
                            return resp
                        else:
                            resp = 'El curso ' + cost_rec[0][0] + ' tiene un ' + cost_rec[0][2] + \
                                   ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[0][4]) + ' dolares americanos.'
                            flg = 0
                            return resp
                    else:
                        resp = 'El curso ' + cost_rec[0][0] + ' tiene un ' + cost_rec[0][2] + \
                               ' igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                               str(cost_rec[0][4]) + ' dolares americanos.'
                        flg = 0
                        return resp
            elif len(cost_rec) == 2:
                if (cost_rec[0][2] == 'COSTO REGULAR') and (cost_rec[1][2] == 'COSTO LIBRE'):
                    if 'nombre_curso_match' in entities_dict.keys():
                        if entities_dict['nombre_curso_match'] != entities_dict['nombre_curso'].lower():
                            resp = 'Quizá te referías al curso ' + cost_rec[0][0] + '. Este puede llevarse de dos formas, como curso LIBRE o ' \
                                                                  'como parte de un MÓDULO. Su ' + cost_rec[0][2] + ' es igual a ' + \
                                   str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[0][4]) + ' dolares americanos. El ' + cost_rec[1][2] + \
                                   ' es igual a ' + str(cost_rec[1][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[1][4]) + ' dolares americanos.'
                            flg = 0
                            return resp
                    else:
                        resp = 'El curso ' + cost_rec[0][0] + ' puede llevarse de dos formas, como curso LIBRE o ' \
                                                              'como parte de un MÓDULO. Su ' + cost_rec[0][
                                   2] + ' es igual a ' + \
                               str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                               str(cost_rec[0][4]) + ' dolares americanos.' 'El ' + cost_rec[1][2] + \
                               ' es igual a ' + str(cost_rec[1][3]) + ' nuevo soles, o lo que equivale a ' + \
                               str(cost_rec[1][4]) + ' dolares americanos.'
                        flg = 0
                        return resp
                else:
                    if 'nombre_curso_match' in entities_dict.keys():
                        if entities_dict['nombre_curso_match'] != entities_dict['nombre_curso'].lower():
                            resp = 'El curso ' + cost_rec[0][0] + ' puede llevarse de dos formas, como curso LIBRE o ' \
                                                                  'como parte de un MÓDULO. Su ' + cost_rec[1][
                                       2] + ' es igual a ' + \
                                   str(cost_rec[1][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[1][4]) + ' dolares americanos y su ' + cost_rec[0][2] + \
                                   ' es igual a ' + str(cost_rec[0][3]) + ' nuevo soles, o lo que equivale a ' + \
                                   str(cost_rec[0][4]) + ' dolares americanos.'
                            flg = 0
                            return resp
            else:
                resp = '¡Lo siento! Por el momento, no dispongo de información sobre los precios de este curso.'
                flg = 0
                return resp
        else:
            resp = 'Lo siento, no logro comprenderle. Por favor, escriba nuevamente su consulta.'
            return resp
    elif flg == 9:
        if cost_rec:
            if cost_rec[0][1] == 'COSTO TOTAL DEL PROGRAMA':
                if 'nombre_programa_match' in entities_dict.keys():
                    if entities_dict['nombre_programa'] != entities_dict['nombre_programa_match'].lower():
                        resp = 'Quizá te referías al programa ' + cost_rec[0][0] + '. Este tiene un costo total de ' + str(cost_rec[0][2]) + \
                               ' nuevos soles, o lo que equivale a ' + str(cost_rec[0][3]) + ' dolares americanos. Aparte, ' \
                                                                                             'tiene un costo de matrícula igual a ' + str(
                            cost_rec[1][2]) + ' nuevo soles, o ' + \
                               str(cost_rec[1][3]) + ' dolares americanos.'
                        flg = 0
                        return resp
                    else:
                        resp = 'El programa ' + cost_rec[0][0] + ' tiene un costo total de ' + str(cost_rec[0][2]) + \
                               ' nuevos soles, o lo que equivale a ' + str(
                            cost_rec[0][3]) + ' dolares americanos. Además, ' \
                                              'tiene un costo de matrícula igual a ' + str(
                            cost_rec[1][2]) + ' nuevo soles, o ' + \
                               str(cost_rec[1][3]) + ' dolares americanos.'
                        flg = 0
                        return resp
                else:
                    resp = 'El programa ' + cost_rec[0][0] + ' tiene un costo total de ' + str(cost_rec[0][2]) + \
                           ' nuevos soles, o lo que equivale a ' + str(
                        cost_rec[0][3]) + ' dolares americanos. Además, ' \
                                          'tiene un costo de matrícula igual a ' + str(
                        cost_rec[1][2]) + ' nuevo soles, o ' + \
                           str(cost_rec[1][3]) + ' dolares americanos.'
                    flg = 0
                    return resp
            else:
                resp = 'El programa ' + cost_rec[1][0] + ' tiene un costo total de ' + str(cost_rec[1][2]) + \
                       ' nuevos soles, o lo que equivale a ' + str(cost_rec[1][3]) + ' dolares americanos. Además, ' \
                                                                                     'tiene un costo de matrícula igual a ' + str(
                    cost_rec[0][2]) + ' nuevo soles, o ' + \
                       str(cost_rec[0][3]) + ' dolares americanos.'
                flg = 0
                return resp
        else:
            resp = 'Lo siento, no logro comprenderle. Por favor, escriba nuevamente su consulta.'
            return resp
    elif flg == 10:
        # Fechas de programación del curso
        f1 = programacion_rec[0][2]
        f2 = programacion_rec[0][3]
        if 'nombre_curso_match' in entities_dict.keys():
            if entities_dict['nombre_curso'] != entities_dict['nombre_curso_match'].lower():
                resp_match = 'Quizá te referías al curso ' + programacion_rec[0][12] + '.'
        # Casos según el estado del curso
        if programacion_rec[0][4] == 1:
            resp = 'El curso ' + programacion_rec[0][12] + ' pertenece al programa ' + cur_en_prog[0][1] + \
                   ', actualmente se encuentra en la condición de ' + estado_cur[0][1] + \
                   ' teniendo como fecha de inicio el ' + f1.strftime("%d-%m-%y") + \
                   ' y fecha prevista de culminación el ' + f2.strftime(
                "%d-%m-%y") + '. Además, tiene una duración de ' + str(programacion_rec[0][16]) + \
                   ' horas calendarias y su horario corresponde a ' + horario_cur[0][1] + ' de ' + horario_cur[0][2] + \
                   ' a ' + horario_cur[0][3] + ' horas.'
            flg = 0
            return resp_match + ' ' + resp
        elif programacion_rec[0][4] == 2:
            resp = 'El curso ' + programacion_rec[0][12] + ' pertenece al programa ' + cur_en_prog[0][1] + \
                   ', actualmente se encuentra ' + estado_cur[0][1] + \
                   '. Tendrá una duración de ' + str(programacion_rec[0][16]) + ' horas calendarias. Se inició el ' + \
                   f1.strftime("%d-%m-%y") + ' y culminará el ' + f2.strftime("%d-%m-%y") + '.'
            flg = 0
            return resp_match + ' ' + resp
        elif programacion_rec[0][4] == 3:
            resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se encuentra ' + estado_cur[0][1] + \
                   ' y no tiene nuevas fechas programadas.'
            flg = 0
            return resp_match + ' ' + resp
        elif programacion_rec[0][4] == 4:
            resp = 'El curso ' + programacion_rec[0][12] + ' se encuentra ' + estado_cur[0][1] + \
                   ' y no se está dictando en la institución.'
            flg = 0
            return resp_match + ' ' + resp
        elif programacion_rec[0][4] == 5:
            resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se encuentra ' + estado_cur[0][1] + '.'
            flg = 0
            return resp_match + ' ' + resp
        elif programacion_rec[0][4] == 6:
            try:
                resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se ha ' + estado_cur[0][1] + \
                       '.' + ' Tendrá una duración de ' + str(programacion_rec[0][16]) + \
                       ' horas calendarias. La nueva fecha de inicio será el ' + reprog_cur[0][0].strftime("%d-%m-%y") + \
                       ' y culminará el ' + reprog_cur[0][1].strftime("%d-%m-%y") + '.'
                flg = 0
                return resp_match + ' ' + resp
            finally:
                pass
        elif programacion_rec[0][4] == 7:
            resp = 'El curso ' + programacion_rec[0][12] + ' actualmente se encuentra ' + estado_cur[0][1] + \
                   ' y por el momento no se está dictando en la institución.'
            flg = 0
            return resp_match + ' ' + resp
    elif flg == 11:
        # Se responde con la fecha de programación del 1er curso (modulo) del programa
        resp = 'El programa ' + row[1] + ' inicia el ' \
               + fec_programa[0][2].strftime("%d-%m-%y") + ' con el primer módulo ' \
               + row[0]
        flg = 0
        return resp
    elif flg == 12:
        # Estas son las respuestas de la intención "otra"
        response = 'Respuesta de flg=12'
        flg = 0
        return response
    elif flg == 13:
        resp_estandar = ['Ok', 'Bien', 'Genial', 'Excelente', 'Está bien', 'Vale']
        response = random.choice(resp_estandar)
        flg = 0
        return response
    elif flg == 14:
        response = 'No logro comprenderle. ¿Podría escribir nuevamente su consulta?'
        flg = 0
        return response
    elif flg == 15:
        response = 'Esta es la intencion continuacion'
        flg = 0
        return response


def chatbot_get_response(user_name, user_mssg):
    connect_params = get_db_info()
    db_connection = DatabaseConnection(connect_params)
    print(db_connection)
    register = []
    path = Path(resource_path('conversations/register_' + user_name + '.json'))
    if path.is_file():
        # Abriendo el archivo JSON para acceder al id
        json_file = open(resource_path('conversations/register_' + user_name + '.json'))
        json_data = json.load(json_file)
        intent_dict, entities_dict = intent_entities_mssg(user_mssg)
        print(intent_dict, entities_dict)
        rec = dict()
        rec['id'] = len(json_data) + 1
        rec['intent'] = intent_dict['intent']
        for key, value in entities_dict.items():
            rec[key] = value
        response_final = conversation_tree(db_connection, intent_dict, entities_dict, json_data)
        with open(resource_path('conversations/register_' + user_name + '.json'), "r+", encoding='utf-8') as file:
            data = json.load(file)
            data.append(rec)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        # Crear el json y guardar el rec
        intent_dict, entities_dict = intent_entities_mssg(user_mssg)
        # print(intent_dict, entities_dict)
        rec = dict()
        rec['id'] = 1
        rec['intent'] = intent_dict['intent']
        for key, value in entities_dict.items():
            rec[key] = value
        register.append(rec)
        with open(resource_path('conversations/register_' + user_name + '.json'), 'w', encoding='utf-8') as file:
            json.dump(register, file, indent=4)
        response_final = conversation_tree(db_connection, intent_dict, entities_dict, [])

    # print('response: ', response_final)
    print(response_final)

    return response_final


if __name__ == "__main__":
    connect_params = get_db_info()
    db_connection = DatabaseConnection(connect_params)
    # user_id = int(sys.argv[1])
    # user_name = sys.argv[1]
    # user_mssg = sys.argv[2]
    user_name = 'jp'
    # user_mssg = 'quiero informacion del curso de camaras de video'
    # user_mssg = 'Quiero informacion sobre diseño de dat center'
    # user_mssg = 'Quiero informacion sobre diseño de data center'
    # user_mssg = 'Quiero información sobre ingeniería de telecomunicaciones'
    # user_mssg = 'Quiero información del programa de ingeniería de telecomunicaciones'
    # user_mssg = 'quiero informacion del curso de ccna'
    # user_mssg = 'quiero informacion del curso de CCTV DIGITALIZADO'
    # user_mssg = 'quiero informacion del curso de sistemas digitales'
    # user_mssg = 'quiero informacion del curso de sistemas satelitales'
    # user_mssg = 'cual es el precio del programa de ingenieria de telecomunicaciones?'
    # user_mssg = 'cual es el precio del programa de ingenieria'
    # user_mssg = 'cual es el precio del curso de sistmas satelitles'
    # user_mssg = 'cual es el precio del curso de sistemas satelitales'
    # user_mssg = 'cual es el precio del curso de SISTEMAS SATELITALES'
    # user_mssg = 'cual es el precio del curso de CCTV DIGITAL'
    # user_mssg = 'cual es el precio del curso de PROPAGACIN Y ANTENAS'
    # user_mssg = 'cual es el precio del curso de COMUNICCIONES MÓVILES'
    # user_mssg = 'cual es el precio del programa de ESPECIALISTA CERTIFICDO EN LINUX'
    # user_mssg = 'cual es el precio?'
    # user_mssg = 'Hola'
    user_mssg = 'cuantas horas se dicta a la semana el curso de comunicaiones móviles?'
    register = []
    path = Path(resource_path('conversations/register_' + user_name + '.json'))
    if path.is_file():
        # Abriendo el archivo JSON para acceder al id
        json_file = open(resource_path('conversations/register_' + user_name + '.json'))
        json_data = json.load(json_file)
        intent_dict, entities_dict = intent_entities_mssg(user_mssg)
        print('i&e_1: ', intent_dict, entities_dict)
        rec = dict()
        rec['id'] = len(json_data) + 1
        rec['intent'] = intent_dict['intent']
        for key, value in entities_dict.items():
            rec[key] = value
        # Agregamos al diccionario entities_dict la entidad coincidente (levenshtein)
        if 'nombre_curso' in entities_dict.keys():
            if db_connection.get_curso(entities_dict['nombre_curso'])[0]:
                if entities_dict['nombre_curso']:
                    entities_dict['nombre_curso_match'] = \
                    (db_connection.get_curso(entities_dict['nombre_curso']))[0][0][1].lower()
                    rec['nombre_curso_match'] = entities_dict['nombre_curso_match']
                else:
                    pass
            else:
                pass
        elif 'nombre_programa' in entities_dict.keys():
            if db_connection.get_programa(entities_dict['nombre_programa'])[0]:
                if entities_dict['nombre_programa']:
                    entities_dict['nombre_programa_match'] = \
                        (db_connection.get_programa(entities_dict['nombre_programa']))[0][0][1].lower()
                    rec['nombre_programa_match'] = entities_dict['nombre_programa_match']
                else:
                    pass
            else:
                pass
        elif ('nombre_curso' in entities_dict.keys()) or ('nombre_programa' in entities_dict.keys()):
            # Codigo para futuras mejoras
            pass
        else:
            pass

        # if ('nombre_curso' in entities_dict.keys()) or ('nombre_programa' in entities_dict.keys()):
        #     if db_connection.get_curso(entities_dict['nombre_curso'])[0]:
        #         if 'nombre_curso' in entities_dict.keys():
        #             if entities_dict['nombre_curso']:
        #                 entities_dict['nombre_curso_match'] = (db_connection.get_curso(entities_dict['nombre_curso']))[0][0][1].lower()
        #                 rec['nombre_curso_match'] = entities_dict['nombre_curso_match']
        #         elif 'nombre_programa' in entities_dict.keys():
        #             if entities_dict['nombre_programa']:
        #                 entities_dict['nombre_programa_match'] = (db_connection.get_curso(entities_dict['nombre_programa']))[0][0][1].lower()
        #                 rec['nombre_programa_match'] = entities_dict['nombre_programa_match']
        #         else:
        #             pass
        #     else:
        #         pass
        # else:
        #     pass
        print('i&e_2: ', intent_dict, entities_dict)
        response_final = conversation_tree(db_connection, intent_dict, entities_dict, json_data)
        with open(resource_path('conversations/register_' + user_name + '.json'), "r+", encoding='utf-8') as file:
            data = json.load(file)
            data.append(rec)
            file.seek(0)
            json.dump(data, file, indent=4)
    else:
        # Crear el json y guardar el rec
        intent_dict, entities_dict = intent_entities_mssg(user_mssg)
        # print(intent_dict, entities_dict)
        rec = dict()
        rec['id'] = 1
        rec['intent'] = intent_dict['intent']
        for key, value in entities_dict.items():
            rec[key] = value
        register.append(rec)
        with open(resource_path('conversations/register_' + user_name + '.json'), 'w', encoding='utf-8') as file:
            json.dump(register, file, indent=4)
        response_final = conversation_tree(db_connection, intent_dict, entities_dict, [])

    # print('response: ', response_final)
    print(response_final)
    # print('rec: ', rec)
