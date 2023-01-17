import logging
import os
from datetime import datetime


def create_folder(path):
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            logger.error("Creation of the dir %s failed" % path)
            print("Creation of the dir %s failed" % path)
            return False
        else:
            print("Successfully created the dir %s " % path)
            logger.info("Successfully created the dir %s " % path)
            return True


logger = logging.getLogger('myLogger')
logger.setLevel(logging.DEBUG)

directory = os.getcwd()
create_folder(directory + "/logs")

today = datetime.now().strftime("%Y%m%d")

handler = logging.FileHandler('./logs/debug_'+str(today)+'.log', 'a', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)