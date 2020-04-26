from OpenSSL import crypto

from .config import Config


def shellman_wizard():
    Config()['connection'] = {
        'host': '0.0.0.0',
        'port': 8080
    }
    Config()['shellman'] = {
        'allow_frontend_to_listen': True
    }

    Config()['tls'] = {}
    Config()['tls']['CN'] = 'localhost'

    print('Generating TLS certificate...')
    cert, key = cert_gen()
    print('Done!')
    Config()['tls']['cert'] = cert
    Config()['tls']['key'] = key

    discord()

    Config().write()


def discord():
    Config()['discord_frontend'] = {
        'token': '',
        'admin_mode': True,
        'guild': 702911703301619742,
        'channel': 702911703301619746,
        'category': 'shells',
        'channel_scheme': 'shellman-'
                          '{shell.connection.writer.get_extra_info("peername")[0].replace(".", "-")}-'
                          '{shell.connection.id}'
    }


def cert_gen():
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
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
