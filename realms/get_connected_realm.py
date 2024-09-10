from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Link:
    href: str

@dataclass
class Self:
    self: Link

@dataclass
class Status:
    type: str
    name: Optional[str]

@dataclass
class Population:
    type: str
    name: Optional[str]

@dataclass
class RegionKey:
    href: str

@dataclass
class Region:
    key: RegionKey
    name: Optional[str]
    id: int

@dataclass
class ConnectedRealm:
    href: str

@dataclass
class RealmType:
    type: str
    name: Optional[str]

@dataclass
class Realm:
    id: int
    region: Region
    connected_realm: ConnectedRealm
    name: Optional[str]
    category: Optional[str]
    locale: str
    timezone: str
    type: RealmType
    is_tournament: bool
    slug: str

@dataclass
class MythicLeaderboards:
    href: str

@dataclass
class Auctions:
    href: str

@dataclass
class ConnectedRealmResponse:
    _links: Self
    id: int
    has_queue: bool
    status: Status
    population: Population
    realms: List[Realm]
    mythic_leaderboards: MythicLeaderboards
    auctions: Auctions

from dataclasses import dataclass
from typing import List
import aiohttp

async def get_connected_realm(region: str, href: str, token: str) -> ConnectedRealmResponse:
    api_url = f"{href}&locale=en_{region}&access_token={token}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                return ConnectedRealmResponse(**data)
            
            return ConnectedRealmResponse(_links=Self(self=Link(href="")), id=0, has_queue=False, 
                                          status=Status(type="", name=None), 
                                          population=Population(type="", name=None), 
                                          realms=[], 
                                          mythic_leaderboards=MythicLeaderboards(href=""), 
                                          auctions=Auctions(href=""))
