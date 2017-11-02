import ssl

__version__ = '0.0.2'

real_match_hostname = ssl.match_hostname


def patched_match_hostname(cert, hostname):
    try:
        return real_match_hostname(cert, hostname)
    except ssl.CertificateError as err:
        try:
            hostname = hostname.encode('idna').decode('ascii')
        except ValueError:
            # no luck to encode, raise previous ssl.CertificateError
            raise err

        return real_match_hostname(cert, hostname)


def patch_match_hostname():
    if hasattr(ssl.match_hostname, 'patched'):
        return

    ssl.match_hostname = patched_match_hostname
    ssl.match_hostname.patched = True


def reset_match_hostname():
    if not hasattr(ssl.match_hostname, 'patched'):
        return

    ssl.match_hostname = real_match_hostname
