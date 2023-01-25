from backend.nlu.nlu import NLU
from backend.conv_manager.question_answering import get_db_info
from backend.database.database_connection import DatabaseConnection
from backend.conv_manager.question_answering import resource_path
from dotenv import load_dotenv
from pathlib import Path
import json
from backend.conv_manager.question_answering import conversation_tree
load_dotenv()
import re

connect_params = get_db_info()
db_connection = DatabaseConnection(connect_params)

class CHATBOT:
    def __init__(self):
        self.nlu = NLU()

    def nlu_inference(self, user_mssg):
        """
        Función que realizará la inferencia del mensaje de usuario enviado desde el frontend para la obtención
        de intencion y entidades
        :param None:
        :return: intent, entities
        """
        output_nlu = self.nlu.inference(user_mssg)
        # intent_dict = {'intent': 'informacion_general'}
        intent_dict = output_nlu["intent"]

        # intent_dict = {'intent': 'informacion_precio'}
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
        # entities_dict = {'nombre_curso': 'CCTV DIGITALIZADO'}
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

    def get_response(self, user_name, user_mssg):
        register = []
        path = Path(resource_path('conversations/register_' + user_name + '.json'))
        if path.is_file():
            # Abriendo el archivo JSON para acceder al id
            json_file = open(resource_path('conversations/register_' + user_name + '.json'))
            json_data = json.load(json_file)
            intent_dict, entities_dict = self.nlu_inference(user_mssg)
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
            intent_dict, entities_dict = self.nlu_inference(user_mssg)
            #print(intent_dict, entities_dict) #intent_entities_mssg
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
