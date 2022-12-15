# -*- coding: utf-8 -*-
"""
@author: Daniel Arteaga, Daniel Urcia
"""

import psycopg2


# ------------------------------------------------------------------
# Clases
# ------------------------------------------------------------------
class DatabaseConnection:
    connection = None
    is_initialized = False
    is_valid_connection = False
    params = None

    def __new__(cls, connect_params, *args, **kwargs):
        if cls.connection is None:
            cls.connection = super(DatabaseConnection, cls).__new__(cls)
        return cls.connection

    def __init__(self, connect_params):
        self.cursor = None
        if not self.is_initialized:
            self.is_valid_connection, self.params = self.connect(connect_params)
            if self.is_valid_connection:
                self.is_initialized = True
            else:
                self.connection = None
        else:
            if self.verify_last_connection(connect_params):
                self.connection.admin.command('ping')
            else:
                self.is_valid_connection, self.params = self.connect(connect_params)
                if self.is_valid_connection:
                    self.connection.admin.command('ping')
                else:
                    self.connection = None
                    self.is_initialized = False

    def connect(self, connect_params):
        user = connect_params['user']
        password = connect_params['password']
        host = connect_params['host']
        database = connect_params['database']
        try:
            self.connection = psycopg2.connect(user=user, password=password, host=host, database=database)
            self.cursor = self.connection.cursor()
            print('conecto')
            return True, connect_params
        except (Exception, psycopg2.Error):
            print('error')
            return False, None

    def verify_last_connection(self, new_params):
        user_condition = (self.params['user'] == new_params['user'])
        password_condition = (self.params['password'] == new_params['password'])
        host_condition = (self.params['host'] == new_params['host'])
        database_condition = (self.params['database'] == new_params['database'])
        if user_condition and password_condition and host_condition and database_condition:
            return True
        else:
            return False

    def get_curso(self, nombre_curso):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """select * from curso where nombre_curso = '{0}'""".format(nombre_curso)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la información del curso. ' + str(error)
        return mobile_records, error_msg

    def get_programa(self, nombre_programa):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """select * from programa where nombre_programa = '{0}'""".format(nombre_programa)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la información del programa. ' + str(error)
        return mobile_records, error_msg

    def get_costo_curso(self, cod_curso):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """SELECT nombre_curso, tipo_curso, nombre_tipo_costo, precio_ref_soles,
                                         precio_ref_dolar
                                         FROM costo_curso a
                                         INNER JOIN curso b ON b.cod_curso = a.cod_curso 
                                         INNER JOIN tipo_costo c ON c.cod_tipo_costo = a.cod_tipo_costo                                
                                         WHERE a.cod_curso = '{0}'""".format(cod_curso)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener el precio del curso. ' + str(error)
        return mobile_records, error_msg

    def get_costo_programa(self, cod_programa):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """SELECT nombre_programa, nombre_tipo_costo, precio_soles,
                                         precio_dolares
                                         FROM costo_programa a
                                         INNER JOIN programa b ON b.cod_programa = a.cod_programa
                                         INNER JOIN tipo_costo c ON c.cod_tipo_costo = a.cod_tipo_costo
                                         WHERE a.cod_programa = '{0}'""".format(cod_programa)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener el precio del programa. ' + str(error)
        return mobile_records, error_msg

    def get_programacion(self, cod_curso):
        programacion_curso = []
        estado_curso = []
        reprog_curso = []
        horario_curso = []
        cur_en_prog = []
        if self.is_valid_connection:
            try:
                select_query = """select * from programacion_curso where cod_curso = '{0}'""".format(cod_curso)
                self.cursor.execute(select_query)
                programacion_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_pc = 'No se pudo obtener la información de la programación del curso. ' + str(error)
                print(error_msg_pc)
            try:
                select_query = """select * from estado_curso where cod_estado_curso = '{0}'""".format(
                    programacion_curso[0][4])
                self.cursor.execute(select_query)
                estado_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_ec = 'No se pudo obtener la información de la programación del curso. ' + str(error)
                print(error_msg_ec)
            try:
                select_query = """SELECT fec_ini_reprog, fec_fin_reprog
                                FROM programacion_curso a
                                INNER JOIN reprogramacion_curso b ON b.cod_prog_curso = a.cod_prog_curso
                                WHERE cod_estado_curso = '{0}' AND cod_curso = '{1}'""".format(estado_curso[0][0],
                                                                                               cod_curso)
                self.cursor.execute(select_query)
                reprog_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_rc = 'No se pudo obtener la información de la programación del curso. ' + str(error)
                print(error_msg_rc)
            try:
                select_query = """SELECT nro_hrs_dia, dia, hora_inicio, hora_fin
                                FROM programacion_curso a
                                INNER JOIN horario_curso b ON b.cod_horario = a.cod_horario
                                WHERE cod_curso = '{0}'""".format(cod_curso)
                self.cursor.execute(select_query)
                horario_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_hc = 'No se pudo obtener la información de la programación del curso. ' + str(error)
                print(error_msg_hc)
            try:
                select_query = """SELECT nro_orden_curso_en_programa, nombre_programa
                                  FROM curso_en_programa a
                                  INNER JOIN programa b ON b.cod_programa = a.cod_programa
                                  WHERE cod_curso = '{0}'""".format(cod_curso)
                self.cursor.execute(select_query)
                cur_en_prog = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_cep = 'No se pudo obtener la información de la programación del curso. ' + str(error)
                print(error_msg_cep)
        return programacion_curso, estado_curso, reprog_curso, horario_curso, cur_en_prog

    def get_date_programa(self, cod_programa):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """SELECT * FROM curso_en_programa WHERE cod_programa ='{0}'""".format(cod_programa)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la información de la programación del curso. ' + str(error)

        for i, element in enumerate(mobile_records):
            if element[1] == 1:
                new_query1 = """SELECT * FROM curso WHERE cod_curso ='{0}'""".format(element[2])
                self.cursor.execute(new_query1)
                records = self.cursor.fetchall()
                new_query2 = """select * from programacion_curso where cod_curso = '{0}'""".format(records[0][0])
                self.cursor.execute(new_query2)
                fecha_curso = self.cursor.fetchall()
                record = [records[0][1], fecha_curso[0][2], fecha_curso[0][3], fecha_curso[0][4]]
                return record, error_msg
            else:
                return [], ''