import ssl

import aiohttp
import pytest

from idna_ssl import PY_370, patch_match_hostname, reset_match_hostname

skip_370 = pytest.mark.skipif(
    PY_370,
    reason='Python>=3.7.0 do not support monkey patching',
)

only_370 = pytest.mark.skipif(
    not PY_370,
    reason='Python>=3.7.0 do not need monkey patching',
)


@skip_370
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


@only_370
@pytest.mark.asyncio
async def test_aiohttp_py370(loop):
    reset_match_hostname()

    url = 'https://цфоут.мвд.рф/news/item/8065038/'

    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            await response.read()

            assert response.status == 200


@skip_370
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

    cert = {'subject': ((('commonName', 'xn--einla-pqa.de'),),)}
    ssl.match_hostname(cert, 'xn--einla-pqa.de')

    cert = {'subject': ((('commonName', 'abc_def.com'),),)}
    ssl.match_hostname(cert, 'abc_def.com')

    cert = {'subject': ((('commonName', '::1'),),)}
    ssl.match_hostname(cert, '::1')


@skip_370
def test_match_hostname_not_py370():
    reset_match_hostname()
    patch_match_hostname()

    cert = {'subject': ((('commonName', 'xn--n1aiccj.xn--b1aew.xn--p1ai'),),)}  # noqa
    ssl.match_hostname(cert, 'цфоут.мвд.рф')

    cert = {'subject': ((('commonName', 'xn--einla-pqa.de'),),)}
    ssl.match_hostname(cert, 'einlaß.de')
