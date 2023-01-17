import requests
import utils
import time
import traceback
import os
import pandas as pd
from setup_logger import logger
from inecrawlerInterface import INECrawlerInterface as interface


class INECrawler(interface):
    
    def __init__(self, domain):
        self.domain = domain

    def get_package_list(self):
        """Get all the packages ids"""
        total_ids = []
        total_ids = utils.get_operations_ids()
        
        return total_ids

    def get_package(self, id):
        """Build a dict of package metadata"""
        # Each operation has n tables; each table has n rows with data; each element has a value and date
        try:
            # Obtaining the tables of the actual operation
            res = requests.get('https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/' + str(id))
            
            if res.status_code == 200:
                metadata = dict()
                metadata['operation_identifier'] = id
                metadata['operation_name'] = utils.get_operation_details(id, 'Nombre')
                metadata['operation_code'] = utils.get_operation_details(id, 'Codigo')
                metadata['operation_cod_IOE'] = utils.get_operation_details(id, 'Cod_IOE')
                
                total_tables_id = []
                
                tables = res.json()
                if len(tables) > 0:
                    
                    table_data_list = []
                    
                    for x in tables:
                        table_data = dict()
                        
                        total_tables_id.append(x['Id'])
                        
                        table_data['identifier'] = x['Id']
                        table_data['name'] = x['Nombre']
                        # if x['Anyo_Periodo_ini']:
                        #     table_data['initial_year'] = x['Anyo_Periodo_ini']
                        # if x['Anyo_Periodo_fin']:
                        #     table_data['last_year'] = x['Anyo_Periodo_fin']
                        table_data['last_modification'] = x['Ultima_Modificacion']
                        
                        # Loop to obtain -> table_data['elements'] 
                        for y in total_tables_id:
                            try:
                                response = requests.get('https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/' + str(y))
                                
                                if response.status_code == 200:
                                    data_json = response.json()
                                    
                                    element_data = dict()
                                    element_data_list = []
                                    
                                    if len(data_json) > 0:
                                        # Loop to obtain -> element_data['data']                                        
                                        for z in data_json:
                                            element_data = dict()
                                            
                                            element_data['filter'] = z['Nombre']
                                            information = z['Data']
                                            
                                            if len(information) > 0:
                                                information_data_list = []
                                                
                                                # Loop to obtain -> element_data['data']
                                                for n in information:
                                                    information_data = dict()
                                                    
                                                    information_data['date'] = n['Fecha']
                                                    information_data['year'] = n['Anyo']
                                                    information_data['month'] = n['FK_Periodo']
                                                    information_data['value'] = n['Valor']
                                                    
                                                    information_data_list.append(information_data)
                                            
                                                element_data['data'] = information_data_list
                                                
                                                # -----------------------------------------------------------
                                                df = pd.DataFrame(information_data_list) # para leer un dict
                                                nombre = z['Nombre'].replace('.', '')
                                                nombre = nombre.replace(' ', '')
                                                nombre = nombre.replace('/', '')
                                                csv = 'C:/Users/Usuario/Desktop/solution/' + nombre + '.csv'
                                                print(csv)
                                                df.to_csv(csv, index=False)
                                                # Guardar un .json con los metadatos
                                                # Libreria para generar un id para que no se repitan los nombres de los archivos
                                                # -----------------------------------------------------------
                                            
                                                element_data_list.append(element_data)
                                        
                            except Exception as e:
                                print(traceback.format_exc())
                                logger.info(e)
                                return None
                        
                        table_data['elements'] = element_data_list
                    
                        table_data_list.append(table_data)
                       
                metadata['operation_tables'] = table_data_list
                
                return metadata
            else:
                return None
        except Exception as e:
            print(traceback.format_exc())
            logger.info(e)
            return None
        
craw = INECrawler('https://servicios.ine.es')
    
 
directorio = "C:/Users/Usuario/Desktop/solution"
try:
    os.stat(directorio)
    file = open(directorio + "/result.txt", "w")
    file.write("Resultado de la consulta" + os.linesep)
    file.write("------------------------" + os.linesep)
    for id in craw.get_package_list():
        print(craw.get_package(id), file=file)
    file.close()
except:
    os.mkdir(directorio)
    

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