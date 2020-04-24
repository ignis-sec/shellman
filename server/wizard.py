from config import Config
from OpenSSL import crypto


def shellman_wizard():
    Config()['connection'] = {
        'host': '0.0.0.0',
        'port': 8080
    }
    Config()['shellman'] = {
        'allow_frontend_to_listen': True
    }

    print("Generating TLS certificate...")
    cert, key = cert_gen()
    print("Done!")
    Config()['tls'] = {
        'cert': cert,
        'key': key
    }

    Config().write()


def cert_gen():
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "KP"
    cert.get_subject().ST = "Pyongyang"
    cert.get_subject().L = "Shellman"
    cert.get_subject().O = "Shellman"
    cert.get_subject().OU = "Shellman"
    cert.get_subject().CN = "Shellman"
    cert.get_subject().emailAddress = "sh@ellm.an"
    cert.set_serial_number(0)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, b'sha512')
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8")
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8")

    return cert, key
