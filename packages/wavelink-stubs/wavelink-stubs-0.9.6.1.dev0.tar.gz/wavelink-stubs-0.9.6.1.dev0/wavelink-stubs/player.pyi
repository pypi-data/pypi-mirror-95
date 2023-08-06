from typing import Any, Dict, Optional, List, TYPE_CHECKING

from discord.ext.commands.bot import BotBase

from .eqs import Equalizer

if TYPE_CHECKING:
    from .node import Node

class Track:
    id: str
    info: Dict[str, Any]
    title: str
    identifier: Optional[str]
    ytid: Optional[str]
    length: int
    duration: int
    uri: Optional[str]
    author: Optional[str]
    is_stream: bool
    thumb: Optional[str]

    @property
    def is_dead(self) -> bool: ...

class TrackPlaylist:
    data: Dict[str, Any]
    tracks: List[Track]

class Player: 

    def __init__(self, bot: BotBase, guild_id: int, node: Node, **kwargs): ...

    @property
    def equalizer(self) -> Equalizer: ...

    @property
    def eq(self) -> Equalizer: ...

    @property
    def is_connected(self) -> bool: ...

    @property
    def is_playing(self) -> bool: ...

    @property
    def is_paused(self) -> bool: ...

    @property
    def position(self) -> int: ...

    async def connect(self, channel_id: int): ...

    async def disconnect(self): ...

    async def play(self, track: Track, *, replace: bool, start: int, end: int): ...

    async def stop(self): ...

    async def destroy(self): ...

    async def set_eq(self, equalizer: Equalizer): ...

    async def set_equalizer(self, equalizer: Equalizer): ...

    async def set_pause(self, pause: bool): ...

    async def set_volume(self, vol: int): ...

    async def seek(self, position: int): ...

    async def change_node(self, identifier: str): ...
