import sys
from json import loads
from os import getenv
from os.path import join, dirname

standard_location = join(dirname(__file__), './config.json')
env_var_config_file_path = getenv('TELEGRAM_PI_BOT_CONFIG', standard_location)

try:
    input_config_file_path = sys.argv[1] if sys.argv and sys.argv[1] else env_var_config_file_path
except IndexError:
    input_config_file_path = env_var_config_file_path

try:
    config_file = open(input_config_file_path, 'r', encoding='utf-8')
except FileNotFoundError:
    print('A config.json file needs to be provided')
    exit(1)

content = loads(config_file.read())

def get(key):
    return content[key]

