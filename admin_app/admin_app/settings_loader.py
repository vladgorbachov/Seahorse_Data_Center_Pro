import configparser
import os


def load_settings():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '..', 'settings.ini'))

    return {
        'DATABASE': {
            'HOST': config['Database']['HOST'],
            'PORT': config['Database']['PORT'],
            'NAME': config['Database']['NAME'],
            'USER': config['Database']['USER'],
            'PASSWORD': config['Database']['PASSWORD'],
        },
        'STATIC_ROOT': config['Paths']['STATIC_ROOT'],
        'MEDIA_ROOT': config['Paths']['MEDIA_ROOT'],
        'SERVER_ADDRESS': config['Server']['ADDRESS'],
    }