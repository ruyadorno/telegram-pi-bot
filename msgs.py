from json import loads
from os.path import join, dirname

def start(key):
    msgFile = open(join(dirname(__file__), './messages.json'), 'r', encoding='utf-8')
    content = loads(msgFile.read())
    l10n_key = key

    def get(key):
        try:
            value = content[key][l10n_key]
        except KeyError:
            value = 'Translation key missing for key: %s' % key
        return value

    return get

