import asyncio
import logging
import random
from typing import Iterable, Any

from aiokit import AioThing


class LeasedItem:
    def __init__(self, pool: "ClientPool"):
        self.pool = pool
        self.client = None

    async def __aenter__(self):
        self.client = await self.pool.free_queue.get()
        logging.getLogger(__name__).info(
            {
                "action": "lease",
                "base_url": self.client.base_url,
                "pool_size": self.pool.free_queue.qsize(),
            }
        )
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.free_queue.put(self.client)


class ClientPool(AioThing):
    def __init__(self, clients_and_weights: Iterable[tuple[Any, int]]):
        super().__init__()
        self.free_queue = asyncio.Queue()
        clients = []
        for client, weight in clients_and_weights:
            clients.extend([client] * weight)
        random.shuffle(clients)
        for client in clients:
            self.free_queue.put_nowait(client)

    @staticmethod
    def from_client(client: Any, par: int):
        return ClientPool((client, par))

    @staticmethod
    def from_pool_config(cls, pool_config):
        clients_and_weights = []
        clients = []
        for client_config in pool_config:
            client = cls(**client_config["config"])
            clients_and_weights.append((client, client_config["weight"]))
            clients.append(client)
        client_pool = ClientPool(clients_and_weights)
        client_pool.starts.extend(clients)
        return client_pool

    def lease(self) -> LeasedItem:
        return LeasedItem(self)
