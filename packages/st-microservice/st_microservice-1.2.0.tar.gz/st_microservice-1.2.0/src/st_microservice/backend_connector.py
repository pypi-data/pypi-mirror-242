from typing import Any

from graphql import GraphQLResolveInfo
import httpx
from st_microservice.request_utils import get_request


async def graphql_call(info: GraphQLResolveInfo, uri: str, query: str, variables: dict[str, Any] | None):
    request = get_request(info)
    headers = {
        'Authorization': 'bearer ' + request.cookies['token']
    }
    client: httpx.AsyncClient = request.app.state.httpx_client
    response = await client.post(
        uri,
        headers=headers,
        json={'query': query, 'variables': variables}
    )
    return response.json()['data']
