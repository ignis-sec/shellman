from config import Config


def shellman_wizard():
    Config()['connection'] = {
        'host': '0.0.0.0',
        'port': 8080
    }
    Config()['shellman'] = {
        'allow_frontend_to_listen': True
    }
    Config().write()
