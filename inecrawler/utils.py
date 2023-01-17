from w3lib.url import url_query_cleaner
from url_normalize import url_normalize
import os
import requests
import traceback
from setup_logger import logger

def clean_url(u):
    """Clean a url string to obtain the mainly domain without protocols."""

    u = url_normalize(u)
    parameters = ['utm_source',
                  'utm_medium',
                  'utm_campaign',
                  'utm_term',
                  'utm_content']

    u = url_query_cleaner(u, parameterlist=parameters,
                          remove=True)

    if u.startswith("http://"):
        u = u[7:]
    if u.startswith("https://"):
        u = u[8:]
    if u.startswith("www."):
        u = u[4:]
    if u.endswith("/"):
        u = u[:-1]
    return u.split('/')[0]

def check_url(url):
    """ Check if exist a well-formed url"""
    if url[:8] == "https://" or url[:7] == "http://":
        return True
    else:
        return False

def lower_list(li):
    """ Convert all element of a list to lowercase"""
    if li:
        return [x.lower() for x in li]
    else:
        return None

def create_folder(path):
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the dir %s failed" % path)
            return False
        else:
            print("Successfully created the dir %s " % path)
            return True
    else:
        return True

def print_intro():

    """ Print the content inside intro.txt"""
    path = os.path.dirname(os.path.abspath(__file__))
    f = open(path + "/intro.txt", "r")
    for x in f:
        print(x, end='')

def load_resume_id(path):
    try:
        f = open(path, "r")
        return f.read()

    except Exception:
        return None

def save_resume_id(path, id):
    f = open(path, "w")
    f.write(id)
    f.close()

def remove_resume_id(path):
    if os.path.exists(path):
        os.remove(path)

def get_operation_details(id, detail):
    try:
        info = ''
        if id:
            response = requests.get('https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES')
            if response.status_code == 200:
                packages = response.json()
                if len(packages) > 0:
                    for p in packages:
                        if p['Id'] == id:
                            if detail == 'Nombre':
                                info = p['Nombre']
                            elif detail == 'Cod_IOE':
                                info = p['Cod_IOE']
                            elif detail == 'Codigo':
                                info = p['Codigo']
        return info
        
    except Exception as e:
        print(traceback.format_exc())
        logger.info(e)
        return None
    
def get_operation_name(id, detail):
    try:
        info = ''
        if id:
            if detail:
                response = requests.get('https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES')
                if response.status_code == 200:
                    operations = response.json()
                    if len(operations) > 0:
                        for p in operations:
                            if p['Id'] == id:
                                if detail == 'Name':
                                    info = p['Nombre']
        return info
        
    except Exception as e:
        print(traceback.format_exc())
        logger.info(e)
        return None
    
def get_table_details(id, detail):
    try:
        info = ''
        if id:
            if detail:
                res = requests.get('https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/' + str(id))
                if res.status_code == 200:
                    tables = res.json()
                    if len(tables) > 0:
                        for p in tables:
                            if p['Id'] == id:
                                if detail == 'Name':
                                    info = p['Nombre']
                                elif detail == 'Modification':
                                    info = p['Ultima_Modificacion']
        return info
    except Exception as e:
        print(traceback.format_exc())
        logger.info(e)
        return None