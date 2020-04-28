import os

from OpenSSL import crypto

from .config import Config

config_dict = {
    'shellman': {
        'host': {
            'default': '0.0.0.0',
            'desc': 'host interface to listen on for incoming tls connections'
        },
        'port': {
            'default': 8080,
            'desc': 'port to listen on for incoming tls connections'
        },
    },
    'tls': {
        'CN': {
            'default': 'localhost',
            'desc': 'hostname to be used for certificate CN, this should be where the target can reach you'
        }
    }
}


def prompt_configs(conf):
    print('Fill out configs: (empty for default, ? for info)')
    for key, subkeys in conf.items():
        Config()[key] = {}
        for subkey in subkeys:
            ask_again = True
            while ask_again:
                v = input(f"[{key}][{subkey}] ({conf[key][subkey]['default']}): ")
                if ask_again := v == '?':
                    print(conf[key][subkey]['desc'])

            Config()[key][subkey] = v or str(conf[key][subkey]['default'])


def shellman_wizard():
    prompt_configs(config_dict)
    cert, key = cert_gen()
    Config()['tls']['cert'] = cert
    Config()['tls']['key'] = key
    Config().write()
    # here, create payloads from templates
    path = f'{os.path.dirname(__file__)}/payloads/'
    payload_file_list = os.listdir(path)
    for file in payload_file_list:
        if file.startswith('.'):
            continue
        with open(path+file, 'rb') as payload:
            pld = payload.read()

        pld = pld.replace(b'HOSTHERE', Config()['tls']['CN'].encode('utf-8'))\
                 .replace(b'PORTHERE', Config()['shellman']['port'].encode('utf-8'))\
                 .replace(b'CERTHERE', Config()['tls']['cert'].encode('utf-8'))

        with open('./'+file, 'wb') as payload:
            payload.write(pld)


def cert_gen():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509()
    cert.get_subject().C = 'KP'
    cert.get_subject().ST = 'Pyongyang'
    cert.get_subject().L = 'Shellman'
    cert.get_subject().O = 'Shellman'
    cert.get_subject().OU = 'Shellman'
    cert.get_subject().CN = Config()['tls']['CN']
    cert.get_subject().emailAddress = 'sh@ellm.an'
    cert.set_serial_number(0)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8')
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode('utf-8')

    return cert, key
