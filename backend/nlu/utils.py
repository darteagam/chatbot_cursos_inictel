import pickle
from dotenv import load_dotenv
import os

load_dotenv()

CHATBOT_HOME = os.getenv('CHATBOT_HOME')

def load_pickle_file(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data


def resource_path(relative_path):
    abs_path = CHATBOT_HOME
    # abs_path = r'C:/Users/user/PycharmProjects/chatbot_cursos_inictel/'
    # abs_path = r'/var/www/html/chatbot_cursos_inictel/'
    return abs_path + relative_path

