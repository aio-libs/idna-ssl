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
