from dataclasses import dataclass
from typing import List
import aiohttp

@dataclass
class Link:
    href: str

@dataclass
class Links:
    self: Link

@dataclass
class ConnectedRealm:
    href: str

@dataclass
class ConnectedRealmsResponse:
    _links: Links
    connected_realms: List[ConnectedRealm]

async def get_all_connected_realms(region: str, token: str) -> ConnectedRealmsResponse:
    api_url = f"https://{region}.api.blizzard.com/data/wow/connected-realm/index?namespace=dynamic-{region}&locale=en_{region.upper()}&access_token={token}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                return ConnectedRealmsResponse(
                    _links=Links(self=Link(href=data["_links"]["self"]["href"])),
                    connected_realms=[ConnectedRealm(href=realm["href"]) for realm in data["connected_realms"]]
                )
            
            return ConnectedRealmsResponse(
                _links=Links(self=Link(href="")),
                connected_realms=[]
            )
