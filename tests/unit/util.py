from typing import AsyncGenerator, Dict, Generator, List

from httpx import Request, Response

from firebolt.client import AsyncClient, Client
from firebolt.client.auth import Auth
from firebolt.model import FireboltBaseModel


def list_to_paginated_response(items: List[FireboltBaseModel]) -> Dict:
    return {"edges": [{"node": i.dict()} for i in items]}


def execute_generator_requests(
    requests: Generator[Request, Response, None], api_endpoint: str = ""
) -> None:
    request = next(requests)

    with Client(
        account_name="account", auth=Auth(), api_endpoint=api_endpoint
    ) as client:
        client._auth = None
        while True:
            response = client.send(request)
            try:
                request = requests.send(response)
            except StopIteration:
                break


async def async_execute_generator_requests(
    requests: AsyncGenerator[Request, Response],
    api_endpoint: str = "",
) -> None:
    request = await requests.__anext__()

    async with AsyncClient(
        account_name="account", auth=Auth(), api_endpoint=api_endpoint
    ) as client:
        client._auth = None
        while True:
            response = await client.send(request)
            try:
                request = await requests.asend(response)
            except StopAsyncIteration:
                break
