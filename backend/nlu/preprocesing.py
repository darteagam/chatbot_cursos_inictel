import re

def preprocess_message(msg):
    """
    Preprocesa el texto del mensaje para la obtención de una lista de tokens.

    :param msg: Texto del mensaje
    :return: preprocessed_msg - Mensaje preprocesado en formato de lista
    """
    # Adición de espacios para separar caracteres especiales al inicio del texto
    temp_msg = re.sub(r'^([^a-zA-Z\d])(.+)$', r'\1 \2', msg)
    # ---------------------------------------------------------------------------------------
    # Adición de espacios para separar caracteres especiales dentro del texto (EXCEPTO: [@_-°#$%&`~^*+<>|¬\{}=[]´])
    # Caso 1: caracteres especiales [,:'/] con significado al encontrarse entre números
    temp_msg = re.sub(r'''(\D)([,:'/])(\D)''', r'\1 \2 \3', temp_msg)
    temp_msg = re.sub(r'''(\d)([,:'/])(\D)''', r'\1 \2 \3', temp_msg)
    temp_msg = re.sub(r'''(\D)([,:'/])(\d)''', r'\1 \2 \3', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 2: caracteres especiales [;"¿?¡!()]
    temp_msg = re.sub(r'([;"¿?¡!()])', r' \1 ', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 3: punto
    temp_msg = re.sub(r'([a-zA-Z\d])(\.) ', r'\1 \2 ', temp_msg)
    temp_msg = re.sub(r' (\.)([a-zA-Z\d])', r' \1 \2', temp_msg)
    # temp_msg = re.sub(r'()(\.)()', r'\1 \2 \3', temp_msg)
    email_match = re.search(r'\w+(?:\.\w+)*@\w+(?:\.\w+)+', temp_msg)
    if email_match:
        l, u = email_match.span()
        pre = temp_msg[:l]
        post = temp_msg[u:]
        new_email = re.sub(r'\.', r'**.**', temp_msg[l:u])
        temp_msg = pre + new_email + post
    temp_msg = re.sub(r'([a-zA-Z])(\.)([a-zA-Z])', r'\1 \2 \3', temp_msg)
    if email_match:
        temp_msg = re.sub(r'\*\*\.\*\*', r'.', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 4: puntos suspensivos
    temp_msg = re.sub(r'\.{3,}', r' Puntos_suspensivoS ', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso 5: �
    temp_msg = re.sub(r'�', r' � ', temp_msg)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # Caso monto y divisas
    temp_msg = re.sub(r'(\b\d+)(s)', r'\1 \2', temp_msg)
    # ---------------------------------------------------------------------------------------
    # Adición de espacios para separar caracteres especiales al final del texto
    temp_msg = re.sub(r'^(.+)([^a-zA-Z\d])$', r'\1 \2', temp_msg, flags=re.M)
    temp_msg = re.sub(r' +', r' ', temp_msg)
    # ---------------------------------------------------------------------------------------
    # Escribir puntos suspensivos
    temp_msg = re.sub(r'Puntos_suspensivoS', r'...', temp_msg)
    # ---------------------------------------------------------------------------------------
    # Separación en tokens
    preprocessed_msg = temp_msg.split()
    return preprocessed_msg


## PreTokenize
def pretokenize(text):
    tokens = preprocess_message(text)
    return tokens