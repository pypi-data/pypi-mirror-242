from typing import Any

from graphql import GraphQLResolveInfo
from httpx import AsyncClient
from st_microservice.request_utils import get_request, get_token


async def graphql_call(info: GraphQLResolveInfo, uri: str, query: str, variables: dict[str, Any] | None = None):
    client: AsyncClient = get_request(info).app.state.httpx_client
    return await send_graphql_request(client, get_token(info), uri, query, variables)


async def send_graphql_request(client: AsyncClient, token: str, uri: str, query: str, variables: dict[str, Any] | None):
    headers = {'Authorization': 'bearer ' + token}
    response = await client.post(uri, headers=headers, json={'query': query, 'variables': variables})
    return response.json()['data']
