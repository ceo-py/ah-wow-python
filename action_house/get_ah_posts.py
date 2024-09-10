import aiohttp
import asyncio
import itertools


def chunked_iterable(iterable: list, size) -> itertools.islice:
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk


async def fetch(session: aiohttp.ClientSession, url: str) -> "json":
    async with session.get(url) as response:
        return await response.json()


def generate_api_url_for_char_fetch(region: str, href: str, token: str) -> str:
    return f"{href[:href.index('?')] + '/auctions'}?namespace=dynamic-{region}&locale=en_{region}&access_token={token}"


async def get_ah_posts(region: str, href: str, token: str):
    api_url = generate_api_url_for_char_fetch(region, href, token)
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                return data

            return []


async def get_ah_posts_multi(tasks: list, token: str):
    responses = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch(session, generate_api_url_for_char_fetch(*data, token))
            for data in tasks
        ]
        for chunk in chunked_iterable(tasks, 100):
            responses += await asyncio.gather(*chunk)
            await asyncio.sleep(3)
    return responses
