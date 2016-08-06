from json import loads
from os import getenv
from os.path import join, dirname

standard_location = join(dirname(__file__), './config.json')
config_file_path = getenv('TELEGRAM_PI_BOT_CONFIG', standard_location)
config_file = open(config_file_path, 'r', encoding='utf-8')
content = loads(config_file.read())

def get(key):
    return content[key]

