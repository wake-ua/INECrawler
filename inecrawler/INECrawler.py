import requests
import utils
import traceback
import uuid
import os
import numpy as np
from setup_logger import logger
from inecrawlerInterface import INECrawlerInterface as interface


class INECrawler(interface):
    
    def __init__(self, domain):
        self.domain = domain
        self.tourism_operations = [61, 62, 63, 132, 180, 238, 239, 240, 241, 328, 329, 330, 334]
        
    def get_operation_list(self):
        """Get all the operations ids"""
        total_ids = []
        response = requests.get('https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES')
        if response.status_code == 200:
            operations = response.json()
            if len(operations) > 0:
                for p in operations:
                    total_ids.append(p['Id'])
        return total_ids

    def get_tables(self, operation_id):
        """Get all the tables ids"""
        try:
            res = requests.get('https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/' + str(operation_id))
            if res.status_code == 200:
                tables = res.json()
                if len(tables) > 0:
                    total_tables = []
                    for x in tables:
                        table = dict()
                        table['id'] = x['Id']
                        table['name'] = x['Nombre']
                        table['modification'] = x['Ultima_Modificacion']
                        total_tables.append(table)
                return total_tables
            else:
                return None
        except Exception as e:
            print(traceback.format_exc())
            logger.info(e)
            return None
    
    def get_elements(self, operation_id, table):
        """Build a dict of elements metadata"""
        operation_name = utils.get_operation_name(operation_id)
        table_id = table['id']
        table_name = table['name']
        modification = table['modification']
        
        try:
            url = 'https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/' + str(table_id)
            response = requests.get(url)

            if response.status_code == 200:
                meta_json = response.json()

                if len(meta_json) > 0:
                    # Loop to obtain -> Element
                    for x in meta_json:
                        metadata = dict()

                        if x.get('COD', None) is not None or x['COD']:
                            metadata['identifier'] = str(operation_id) + '_' + str(table_id) + '_' + str(x.get('COD', None))
                            metadata['title'] = operation_name + ':' + table_name
                            metadata['description'] = operation_name + ': ' + table_name + '. Valores: ' + x.get('Nombre', None)
                            if operation_id in self.tourism_operations:
                                metadata['theme'] = 'Turismo'
                            else:
                                metadata['theme'] = None

                            # ------------------------------------
                            data = x.get('Data', None)
                            if len(data) > 0:
                                resource_list = []
                                
                                for y in data:
                                    information_data = dict()

                                    information_data['id'] = str(x.get('COD', '-'))
                                    information_data['name'] = x.get('Nombre', '-')
                                    information_data['date'] = str(y.get('Fecha', '-'))
                                    information_data['year'] = y.get('Anyo', '-')
                                    information_data['month'] = y.get('FK_Periodo', '-')
                                    information_data['value'] = y.get('Valor', '-')

                                    resource_list.append(information_data)
                                metadata['resources'] = resource_list
                                nombre = x['Nombre'].replace('.', '')
                                nombre = nombre.replace(' ', '')
                                nombre = nombre.replace('/', '')
                                uid = str(uuid.uuid4()).replace('-', '')
                                metadata['filename'] = nombre + uid + '.csv'
                            else:
                                metadata['resources'] = []
                                metadata['filename'] = ''
                            metadata['modified'] = str(modification)
                            metadata['url'] = url
                            metadata['license'] = 'INE License'
                            metadata['source'] = 'https://servicios.ine.es'
                return metadata

        except Exception as e:
            print(traceback.format_exc())
            logger.info(e)
            return None

# Schema:    
# Object -> operation id
#        -> operation name
#        -> operation tables -> id
#                            -> filter
#                            -> year
#                            -> last modification
#                            -> elements          -> name
#                                                 -> data.csv (descargar .json)-> date
#                                                                              -> year
#                                                                              -> month
#                                                                              -> value