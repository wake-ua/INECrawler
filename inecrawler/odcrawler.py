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

    def __init__(self, domain, path, operation_id, tourism_operations, theme):
        self.domain = domain
        if not path:
            directory = os.getcwd()
            path = directory + '/data/'
            utils.create_folder(path)
        self.save_path = path + utils.clean_url(self.domain)
        self.resume_path = path + "resume_"+utils.clean_url(self.domain)+".txt"
        
        self.tourism_operations = tourism_operations
        if operation_id:
            self.operation_id = operation_id
        else:
            None
        if theme:
            self.theme = theme
        
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
        
   

    def save_dataset(self, url, ext):
        """ Save a dataset from a given url and extension"""
        try:
            # Web page is not consideret a dataset
            if url[-4] != 'html':

                logger.info("Saving... %s ", url)

                with requests.get(url, stream=True, timeout=60, verify=False) as r:
                    if r.status_code == 200:
                        # Try to obtain the file name inside the link, else
                        # use the last part of the url with the dataset extension
                        if "Content-Disposition" in r.headers.keys():
                            fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
                        else:
                            fname = url.split("/")[-1]
                            if len(fname.split(".")) == 1:
                                fname += "."+ext

                        path = self.save_path+"/"+fname.replace('"', '')

                        # Write the content on a file
                        with open(path, 'wb') as outfile:
                            t = time.time()
                            partial = False
                            for chunk in r.iter_content(chunk_size=1024):

                                if self.max_sec and ((time.time() - t) > self.max_sec):
                                    partial = True
                                    logger.warning('Timeout! Partially downloaded file %s', url)
                                    break

                                if chunk:
                                    outfile.write(chunk)
                                    outfile.flush()

                        if not partial:
                            logger.info("Dataset saved from %s", url)

                        return path
                    else:
                        logger.warning('Problem obtaining the resource %s', url)

                        return None

        except Exception as e:
            logger.error('Error saving dataset from %s', url)
            logger.error(e)
            return None

    def save_metadata(self, data):
        """ Save the dict containing the metadata on a json file"""
        try:
            with open(self.save_path + "/meta_"+str(data['identifier'])+'.json',
                      'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error('Error saving metadata  %s',
                         self.save_path + "/meta_"+data['identifier']+'.json')
            logger.error(e)

    def get_operation_list(self):
        return self.dms_instance.get_operation_list()
    def get_tables(self, id):
        return self.dms_instance.get_tables(id)
    def get_elements(self, operation_id, table_id):
        return self.dms_instance.get_elements(operation_id, table_id)