import ssl

import aiohttp
import pytest

from idna_ssl import patch_match_hostname, reset_match_hostname


@pytest.mark.asyncio
async def test_aiohttp(loop):
    reset_match_hostname()

    url = 'https://цфоут.мвд.рф/news/item/8065038/'

    with pytest.raises(aiohttp.ClientConnectorCertificateError):
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(url) as response:
                await response.read()

    patch_match_hostname()

    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            await response.read()

            assert response.status == 200


def test_patch():
    reset_match_hostname()

    assert not hasattr(ssl.match_hostname, 'patched')

    patch_match_hostname()

    assert hasattr(ssl.match_hostname, 'patched')

    patch_match_hostname()

    assert hasattr(ssl.match_hostname, 'patched')

    reset_match_hostname()

    assert not hasattr(ssl.match_hostname, 'patched')

    reset_match_hostname()

    assert not hasattr(ssl.match_hostname, 'patched')


def test_match_hostname():
    reset_match_hostname()
    patch_match_hostname()

    cert = {'subject': ((('commonName', 'xn--n1aiccj.xn--b1aew.xn--p1ai'),),)}
    ssl.match_hostname(cert, 'xn--n1aiccj.xn--b1aew.xn--p1ai')

    cert = {'subject': ((('commonName', 'xn--n1aiccj.xn--b1aew.xn--p1ai'),),)}
    ssl.match_hostname(cert, 'цфоут.мвд.рф')

    cert = {'subject': ((('commonName', 'xn--einla-pqa.de'),),)}
    ssl.match_hostname(cert, 'einlaß.de')

    cert = {'subject': ((('commonName', 'xn--einla-pqa.de'),),)}
    ssl.match_hostname(cert, 'xn--einla-pqa.de')

    cert = {'subject': ((('commonName', 'abc_def.com'),),)}
    ssl.match_hostname(cert, 'abc_def.com')

    cert = {'subject': ((('commonName', '::1'),),)}
    ssl.match_hostname(cert, '::1')
