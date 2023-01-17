import requests
import utils
import traceback
import uuid
import pandas as pd
from setup_logger import logger
from inecrawlerInterface import INECrawlerInterface as interface


class INECrawler(interface):
    
    def __init__(self, domain):
        self.domain = domain
        
    def get_operation_list(self):
        """Get all the operations ids"""
        total_ids = []
        # response = requests.get('https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES')
        # if response.status_code == 200:
        #     operations = response.json()
        #     if len(operations) > 0:
        #         for p in operations:
        #             total_ids.append(p['Id'])
        total_ids = [61]
        return total_ids

    def get_tables(self, operation_id):
        """Get all the tables ids"""
        try:
            res = requests.get('https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/' + str(operation_id))
            if res.status_code == 200:
                total_ids = []
                tables = res.json()
                if len(tables) > 0:
                    for x in tables:
                        total_ids.append(x['Id'])
                return total_ids
            else:
                return None
        except Exception as e:
            print(traceback.format_exc())
            logger.info(e)
            return None
    
    def get_elements(self, operation_id, table_id):
        """Build a dict of elements metadata"""
        try:
            response = requests.get('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/' + str(table_id))

            if response.status_code == 200:
                meta_json = response.json()

                element_data_list = []

                if len(meta_json) > 0:
                    # Loop to obtain -> Element
                    for x in meta_json:
                        metadata = dict()

                        metadata['identifier'] = str(operation_id) + '_' + str(table_id) + '_' + x['COD']
                        metadata['title'] = utils.get_operation_name(operation_id, 'Name') + ': ' + utils.get_table_details(table_id, 'Name')
                        metadata['description'] = 'Datos de la operación ' + str(operation_id) + ': ' + utils.get_operation_name(operation_id, 'Name') + ', Tabla ' + str(table_id) + ': ' + utils.get_table_details(table_id, 'Name') + ', Elemento ' + x['Nombre']
                        if operation_id in self.tourism_operations:
                            metadata['theme'] = 'Turismo'
                        else:
                            metadata['theme'] = '-'

                        # ------------------------------------
                        data = x['Data']
                        if len(data) > 0:
                            resource_list = []
                            
                            for y in data:
                                information_data = dict()

                                information_data['id'] = x['COD']
                                information_data['name'] = x['Nombre']
                                information_data['date'] = y['Fecha']
                                information_data['year'] = y['Anyo']
                                information_data['month'] = y['FK_Periodo']
                                information_data['value'] = y['Valor']

                                resource_list.append(information_data)
                            metadata['resources'] = resource_list
                            # -----------------------------------------------------------
                            # para leer un dict
                            df = pd.DataFrame(resource_list)
                            nombre = x['Nombre'].replace('.', '')
                            nombre = nombre.replace(' ', '')
                            nombre = nombre.replace('/', '')
                            uid = str(uuid.uuid4()).replace('-', '')
                            csv = 'C:/Users/Usuario/Desktop/solution/' + nombre + uid + '.csv'
                            print(csv)
                            df.to_csv(csv, index=False)
                            # Guardar un .json con los metadatos
                            # Libreria para generar un id para que no se repitan los nombres de los archivos
                            # -----------------------------------------------------------
                        else:
                            metadata['resources'] = None
                        # ------------------------------------
                        metadata['modified'] = utils.get_table_details(table_id, 'Modification')
                        metadata['license'] = 'INE License'
                        metadata['source'] = 'https://servicios.ine.es'

        except Exception as e:
            print(traceback.format_exc())
            logger.info(e)
            return None
        
# craw = INECrawler('https://servicios.ine.es')
    
 
# directorio = "C:/Users/Usuario/Desktop/solution"
# try:
#     os.stat(directorio)
#     file = open(directorio + "/result.txt", "w")
#     file.write("Resultado de la consulta" + os.linesep)
#     file.write("------------------------" + os.linesep)
#     for operation_id in craw.get_operation_list():
#         for table_id in craw.get_tables(operation_id):
#             print(craw.get_elements(operation_id, table_id), file=file)
#     file.close()
# except:
#     os.mkdir(directorio)
    

# Schema:    
# Object -> operation id
#        -> operation name
#        -> operation tables -> id
#                            -> filter
#                            -> year
#                            -> last modification
#                            -> elements          -> name
#                                                 -> data.csv (descargar .csv) -> date
#                                                                              -> year
#                                                                              -> month
#                                                                              -> value

# Concatenar 3 id "_"
# Nombre elemento: Operacion + Tabla
# Descripcion: Operacion + Tabla + Elemento
# Keywords: -
# Theme: Turismo
# Resources: nombreArchivo.csv
# LastModification: ultima modificacion
# Licencia: Licencia INE (preguntar a Norberto cuál usa el INE)
# Source: url INE