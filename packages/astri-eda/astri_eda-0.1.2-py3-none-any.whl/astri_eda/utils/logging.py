# -*- coding: utf-8 -*-

import logging
import time
import os

def build_logger(log_folder):
    log_name = time.strftime("%Y-%m-%d_%H_%M_%S")+'.log'
    file = os.path.join(log_folder,log_name)

    if os.path.exists(file):
        os.remove(file)


    logging.basicConfig(level=logging.DEBUG,
                        filename=file,
                        datefmt='%Y/%m/%d %H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')


    logger = logging.getLogger(__name__)
    return logger