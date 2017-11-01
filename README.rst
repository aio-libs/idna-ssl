idna_ssl
========

:info: Patch ssl.match_hostname for Unicode(inda) domains support

.. image:: https://travis-ci.org/wikibusiness/idna_ssl.svg?branch=master
    :target: https://travis-ci.org/wikibusiness/idna_ssl

.. image:: https://img.shields.io/pypi/v/idna_ssl.svg
    :target: https://pypi.python.org/pypi/idna_ssl

.. image:: https://codecov.io/gh/wikibusiness/idna_ssl/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/wikibusiness/idna_ssl

Installation
------------

.. code-block:: shell

    pip install idna_ssl

Usage
-----

.. code-block:: python

    from idna_ssl import patch_match_hostname  # noqa isort:skip
    patch_match_hostname()  # noqa isort:skip

    import asyncio

    import aiohttp

    URL = 'https://цфоут.мвд.рф/news/item/8065038/'


    async def main():
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                print(response)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Motivation
----------

* Related aiohttp `issue <https://github.com/aio-libs/aiohttp/issues/949>`_
* It is not fixed yet (by November 2017) in python itself
