import logging
import os

#function to create logger with all logging levels and saves to a folder called logs with a file name (name).log
def create_logger(name):

    delete_log(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages 
    fh = logging.FileHandler('logs/' + name + '.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger



#function to delete the log file given a log file name
def delete_log(name):
    
    print("log deleted")