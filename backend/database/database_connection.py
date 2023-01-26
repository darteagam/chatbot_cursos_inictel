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
            return True, connect_params
        except (Exception, psycopg2.Error):
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

    def get_curso(self, nombre_cur):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                # select_query = """select * from curso where nombre_curso = '{0}'""".format(nombre_cur)
                select_query = """SELECT *, levenshtein(lower(nombre_curso), lower('{0}'))
                                  AS levenshtein_distance FROM curso ORDER BY levenshtein_distance
                                  ASC LIMIT 5""".format(nombre_cur)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
                # print(mobile_records)
                if mobile_records:
                    if mobile_records[0][-1] == 0:
                        mobile_records = [mobile_records[0]]
                        error_msg = 'dist_cero'
                    elif mobile_records[0][-1] <= (len(nombre_cur)//3 + 1):
                    # elif mobile_records[0][-1] < (len(nombre_cur)//3):
                        mobile_records = [mobile_records[0]]
                        error_msg = '--'
                    else:
                        mobile_records = []
                        error_msg = 'Lo siento, no he encontrado informacion referida a ese curso. ' \
                                    'Por favor, escriba nuevamente su consulta.'
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la información del curso. ' + str(error)
        return mobile_records, error_msg

    def get_programa(self, nombre_prog):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                # select_query = """select * from programa where lower(nombre_programa) = '{0}'""".format(nombre_programa)
                select_query = """SELECT *, levenshtein(lower(nombre_programa), lower('{0}'))
                                 AS levenshtein_distance FROM programa ORDER BY levenshtein_distance 
                                 ASC LIMIT 5""".format(nombre_prog)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
                if mobile_records:
                    if mobile_records[0][-1] == 0:
                        mobile_records = [mobile_records[0]]
                        error_msg = 'dist_cero'
                    elif mobile_records[0][-1] < (len(nombre_prog) // 3 + 1):
                        mobile_records = [mobile_records[0]]
                        error_msg = '--'
                    else:
                        mobile_records = []
                        error_msg = 'Lo siento, no he encontrado informacion referida a ese programa. ' \
                                    'Por favor, escriba nuevamente su consulta.'
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la información del programa. ' + str(error)
        return mobile_records, error_msg

    def get_costo_curso(self, nombre_curso):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """SELECT nombre_curso, tipo_curso, nombre_tipo_costo, precio_ref_soles,
                                         precio_ref_dolar
                                         FROM costo_curso a
                                         INNER JOIN curso b ON b.cod_curso = a.cod_curso 
                                         INNER JOIN tipo_costo c ON c.cod_tipo_costo = a.cod_tipo_costo                                
                                         WHERE lower(b.nombre_curso) = '{0}'""".format(nombre_curso.lower())
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener el precio del curso. ' + str(error)
        return mobile_records, error_msg

    # def get_costo_curso(self, nombre_cur):
    #     mobile_records = []
    #     error_msg = ''
    #     if self.is_valid_connection:
    #         try:
    #             select_query = """SELECT nombre_curso, tipo_curso, nombre_tipo_costo, precio_ref_soles,
    #                                      precio_ref_dolar, levenshtein(lower(nombre_curso), lower('{0}'))
    #                                      AS levenshtein_distance
    #                                      FROM costo_curso a
    #                                      INNER JOIN curso b ON b.cod_curso = a.cod_curso
    #                                      INNER JOIN tipo_costo c ON c.cod_tipo_costo = a.cod_tipo_costo
    #                                      WHERE lower(b.nombre_curso) = '{0}' ORDER BY levenshtein_distance
    #                                      ASC LIMIT 5""".format(nombre_cur)
    #             self.cursor.execute(select_query)
    #             mobile_records = self.cursor.fetchall()
    #             if mobile_records:
    #                 if mobile_records[0][-1] == 0:
    #                     mobile_records = [mobile_records[0]]
    #                     error_msg = 'dist_cero'
    #                 elif mobile_records[0][-1] < (len(nombre_cur)//3):
    #                     mobile_records = [mobile_records[0]]
    #                     error_msg = '--'
    #                 else:
    #                     mobile_records = []
    #                     error_msg = 'Lo siento, no he encontrado informacion referida a ese curso. ' \
    #                                 'Por favor, escriba nuevamente su consulta.'
    #         except (Exception, psycopg2.Error) as error:
    #             error_msg = 'No se pudo obtener el precio del curso. ' + str(error)
    #     return mobile_records, error_msg

    def get_costo_programa(self, nombre_programa):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """SELECT nombre_programa, nombre_tipo_costo, precio_soles,
                                         precio_dolares
                                         FROM costo_programa a
                                         INNER JOIN programa b ON b.cod_programa = a.cod_programa
                                         INNER JOIN tipo_costo c ON c.cod_tipo_costo = a.cod_tipo_costo
                                         WHERE lower(b.nombre_programa) = '{0}'""".format(nombre_programa.lower())
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener el precio del programa. ' + str(error)
        return mobile_records, error_msg

    # def get_costo_programa(self, nombre_prog):
    #     mobile_records = []
    #     error_msg = ''
    #     if self.is_valid_connection:
    #         try:
    #             select_query = """SELECT nombre_programa, nombre_tipo_costo, precio_soles,
    #                                      precio_dolares, levenshtein(lower(nombre_programa), lower('{0}'))
    #                                      AS levenshtein_distance
    #                                      FROM costo_programa a
    #                                      INNER JOIN programa b ON b.cod_programa = a.cod_programa
    #                                      INNER JOIN tipo_costo c ON c.cod_tipo_costo = a.cod_tipo_costo
    #                                      WHERE lower(b.nombre_programa) = '{0}' ORDER BY levenshtein_distance
    #                                      ASC LIMIT 5""".format(nombre_prog)
    #             self.cursor.execute(select_query)
    #             mobile_records = self.cursor.fetchall()
    #             if mobile_records:
    #                 if mobile_records[0][-1] == 0:
    #                     mobile_records = [mobile_records[0]]
    #                     error_msg = 'dist_cero'
    #                 elif mobile_records[0][-1] < (len(nombre_prog)//3):
    #                     mobile_records = [mobile_records[0]]
    #                     error_msg = '--'
    #                 else:
    #                     mobile_records = []
    #                     error_msg = 'Lo siento, no he encontrado informacion referida a ese curso. ' \
    #                                 'Por favor, escriba nuevamente su consulta.'
    #         except (Exception, psycopg2.Error) as error:
    #             error_msg = 'No se pudo obtener el precio del programa. ' + str(error)
    #     return mobile_records, error_msg

    def get_programacion(self, nombre_curso):
        programacion_curso = []
        estado_curso = []
        reprog_curso = []
        horario_curso = []
        cur_en_prog = []
        if self.is_valid_connection:
            try:
                select_query = """select * from programacion_curso a inner join curso b on b.cod_curso = a.cod_curso 
                                  where lower(b.nombre_curso) = '{0}'""".format(nombre_curso.lower())
                self.cursor.execute(select_query)
                programacion_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_pc = 'No se pudo obtener la información de la programación del curso. ' + str(error)
            try:
                select_query = """select * from estado_curso where cod_estado_curso = '{0}'""".format(
                    programacion_curso[0][4])
                self.cursor.execute(select_query)
                estado_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_ec = 'No se pudo obtener la información de la programación del curso. ' + str(error)
            try:
                select_query = """SELECT fec_ini_reprog, fec_fin_reprog
                                FROM programacion_curso a
                                INNER JOIN reprogramacion_curso b ON b.cod_prog_curso = a.cod_prog_curso
                                INNER JOIN curso c ON c.cod_curso = a.cod_curso
                                WHERE lower(nombre_curso) = '{0}'""".format(nombre_curso.lower())
                self.cursor.execute(select_query)
                reprog_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_rc = 'No se pudo obtener la información de la programación del curso. ' + str(error)
            try:
                select_query = """SELECT nro_hrs_dia, dia, hora_inicio, hora_fin
                                FROM programacion_curso a
                                INNER JOIN horario_curso b ON b.cod_horario = a.cod_horario
                                INNER JOIN curso c ON c.cod_curso = a.cod_curso
                                WHERE lower(nombre_curso) = '{0}'""".format(nombre_curso.lower())
                self.cursor.execute(select_query)
                horario_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_hc = 'No se pudo obtener la información de la programación del curso. ' + str(error)
            try:
                select_query = """SELECT nro_orden_curso_en_programa, nombre_programa
                                  FROM curso_en_programa a
                                  INNER JOIN programa b ON b.cod_programa = a.cod_programa
                                  INNER JOIN curso c ON c.cod_curso = a.cod_curso
                                  WHERE lower(nombre_curso) = '{0}'""".format(nombre_curso.lower())
                self.cursor.execute(select_query)
                cur_en_prog = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg_cep = 'No se pudo obtener la información de la programación del curso. ' + str(error)
        return programacion_curso, estado_curso, reprog_curso, horario_curso, cur_en_prog

    def get_date_programa(self, nombre_programa):
        mobile_records = []
        error_msg = ''
        if self.is_valid_connection:
            try:
                select_query = """SELECT cod_curso FROM curso_en_programa a
                                  INNER JOIN programa b ON b.cod_programa = a.cod_programa
                                  WHERE nombre_programa ='{0}' ORDER BY nro_orden_curso_en_programa""".format(nombre_programa)
                self.cursor.execute(select_query)
                mobile_records = self.cursor.fetchall()
                cod_curso = mobile_records[0][0]
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la información de la programación del curso. ' + str(error)
            try:
                select_query = """SELECT nombre_curso FROM curso WHERE cod_curso ='{0}'""".format(cod_curso)
                self.cursor.execute(select_query)
                nombre_curso = self.cursor.fetchall()[0][0]
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la información del nombre del curso. ' + str(error)
            try:
                select_query = """select * from programacion_curso where cod_curso = '{0}'""".format(cod_curso)
                self.cursor.execute(select_query)
                fecha_curso = self.cursor.fetchall()
            except (Exception, psycopg2.Error) as error:
                error_msg = 'No se pudo obtener la fecha del curso. ' + str(error)
            return fecha_curso, nombre_curso, error_msg
