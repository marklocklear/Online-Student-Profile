import os

from django.utils import simplejson as json

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_ROOT = os.path.join(APP_ROOT, 'data')

def load_json_data(json_file):
    f = file(os.path.join(DATA_ROOT, json_file))
    data = f.read()
    data = json.loads(data)
    f.close()

    return data
