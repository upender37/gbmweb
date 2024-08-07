
import os
import csv
import time
import logging



DATA_FOLDER_PATH = 'data'
EXTRACT_RESULTS_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'businesses')
LOG_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'log')


def get_logger(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    f_handler = logging.FileHandler(
        os.path.join(LOG_FOLDER_PATH, name + '.log'), encoding='utf-8'
    )
    f_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
    _logger.addHandler(f_handler)
    return _logger


def write_result(result: dict, file_path=None):
    if not file_path:
        file_path = os.path.join(EXTRACT_RESULTS_FOLDER_PATH, time.strftime('%Y %m %d') + '.csv')
    write_header = not os.path.isfile(file_path)
    with open(file_path, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=result.keys())
        if write_header:
            csv_writer.writeheader()
        csv_writer.writerow(result)


for path in [DATA_FOLDER_PATH, EXTRACT_RESULTS_FOLDER_PATH, LOG_FOLDER_PATH]:
    os.makedirs(path, exist_ok=True)
main_logger = get_logger('gbm')




