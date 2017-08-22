# Elastic Search global settings
# https://elasticsearch-dsl.readthedocs.io/en/latest/configuration.html
# http://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
import os
from django.conf import settings


DATABASE_CONNECTION_INFO = {
    'hosts': ['localhost'],
    # 'PORT': None,
    # 'timeout': 100
}

INDEX_SETTINGS = {

}

INDEX_NAME = 'tpddl8'

# SCRAPPER_FOLDER_STRUCTURE = {
#     'A': 'scrappers_miners.API_struct_data',
#     'S': 'scrappers_miners.API_unstruct_data',
#     'C': 'scrappers_miners.no_API'
# }

data_files = [
    "CSMD.csv",
    "CSMD2.csv",
]

error_file = "log_errors.txt"

key_mapping = {
    "Bic Zdistric": "district",
    "Bic Zone": "zone_code",
    "Bic Zone Text": "zone",
    "Bic Zvkont": "vkont",
    "Bic Zinstlion": "instlion",
    "Bic Zfullnam": "full_name",
    "Bic Zsupply": "supply",
    "Bic Zbilladr": "billing_address",

}

DATA_PATH = os.path.join(settings.BASE_DIR, 'data')

es_result_size = 10
