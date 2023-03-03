import requests
import urllib3
import json
import utils
import re
import os
import time
from INECrawler import INECrawler
from setup_logger import logger
from sys import exit


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OpenDataCrawler():

    def __init__(self, domain, operation_id, theme, year, path):
        self.domain = domain
        
        if not path:
            directory = os.getcwd()
            path = os.path.join(directory, 'data')
            utils.create_folder(path)
        
        if operation_id:
            self.operation_id = operation_id
        else:
            self.operation_id = None
            
        if year:
            self.year = year
        else:
            self.year = None
            
        if theme:
            self.theme = theme
        else:
            self.theme = None
             
        self.save_path =os.path.join(path, utils.clean_url(self.domain))

        
        self.resume_path = os.path.join(path, "resume_"+utils.clean_url(self.domain)+".txt")
        
        print("Detecting DMS")
        self.detect_dms()

    def detect_dms(self):
        """Detect the domain DMS and create and instantece according to it"""
        dms = dict()

        dms['INE'] = '/wstempus/js/ES/OPERACIONES_DISPONIBLES'

        for k, v in dms.items():
            try:
                # Delete / if exist
                if self.domain[-1] == "/":
                    self.domain = self.domain[:-1]

                response = requests.get(self.domain+v, verify=False)
                # If the content-type not is a webpage(we want a json api response) and the result code is 200
                if response.status_code == 200 and response.headers['Content-Type']!="text/html":
                    self.dms = k
                    logger.info("DMS detected %s", k)

                    if not utils.create_folder(self.save_path):
                        logger.info("Can't create folder" + self.save_path)
                        exit()
                    break
            except Exception as e:
                logger.info(e)

        # Create an instance of the corresponding dms
        if self.dms == 'INE':
            self.dms_instance = INECrawler(self.domain)
        if self.dms is None:
            print("The domain " + self.domain + " is not supported")
            logger.info("DMS not detected in %s", self.domain)


    def save_metadata(self, data):
        """ Save the dict containing the metadata on a json file"""
        try:
            with open(self.save_path + "/meta_"+ data['identifier'] + '.json',
                      'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error('Error saving metadata  %s',
                         self.save_path + "/meta_" + data['identifier'] + '.json')
            logger.error(e)
            
    def save_dataset(self, data):
        """ Save the dict containing the metadata on a json file"""
        try:
            with open(self.save_path + '/' + data['filename'],
                      'w', encoding='utf-8') as f:
                json.dump(data['resources'], f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error('Error saving metadata  %s',
                         self.save_path + '/' + data['filename'])
            logger.error(e)
            
    def save_partial_dataset(self, data):
        """ Save a dataset from a given url and extension"""
        # Write the partial content on a file
        path = self.save_path + '/' + data['filename']
        logger.info("Path: %s", path)

        try:
            cont = 0
            lines = []
            with open(self.save_path + '/' + data['filename'],
                      'w', encoding='utf-8') as f:
                logger.info('Tamaño resources: %s', len(data['resources']))
                for i in data['resources']:
                    if cont < 10:
                        lines.append(i)
                        cont += 1
                    else:
                        break
                json.dump(lines, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error('Error saving metadata  %s',
                         self.save_path + '/' + data['filename'])
            logger.error(e)

    def get_operation_list(self):
        return self.dms_instance.get_operation_list()
    def get_tables(self, id):
        return self.dms_instance.get_tables(id)
    def get_elements(self, operation_id, table_id):
        return self.dms_instance.get_elements(operation_id, table_id)