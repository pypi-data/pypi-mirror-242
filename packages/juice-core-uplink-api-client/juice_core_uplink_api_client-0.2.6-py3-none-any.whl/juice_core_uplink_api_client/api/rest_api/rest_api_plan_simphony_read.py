from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rest_api_plan_simphony_read_mode import RestApiPlanSimphonyReadMode
from ...models.simphony_plan import SimphonyPlan
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    mode: Union[Unset, None, RestApiPlanSimphonyReadMode] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["start"] = start

    params["end"] = end

    json_mode: Union[Unset, None, str] = UNSET
    if not isinstance(mode, Unset):
        json_mode = mode.value if mode else None

    params["mode"] = json_mode

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/rest_api/plan_simphony/{id}/".format(
            id=id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, SimphonyPlan]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SimphonyPlan.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, SimphonyPlan]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    mode: Union[Unset, None, RestApiPlanSimphonyReadMode] = UNSET,
) -> Response[Union[Any, SimphonyPlan]]:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
        mode (Union[Unset, None, RestApiPlanSimphonyReadMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SimphonyPlan]]
    """

    kwargs = _get_kwargs(
        id=id,
        start=start,
        end=end,
        mode=mode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    mode: Union[Unset, None, RestApiPlanSimphonyReadMode] = UNSET,
) -> Optional[Union[Any, SimphonyPlan]]:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
        mode (Union[Unset, None, RestApiPlanSimphonyReadMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SimphonyPlan]
    """

    return sync_detailed(
        id=id,
        client=client,
        start=start,
        end=end,
        mode=mode,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    mode: Union[Unset, None, RestApiPlanSimphonyReadMode] = UNSET,
) -> Response[Union[Any, SimphonyPlan]]:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
        mode (Union[Unset, None, RestApiPlanSimphonyReadMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SimphonyPlan]]
    """

    kwargs = _get_kwargs(
        id=id,
        start=start,
        end=end,
        mode=mode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    mode: Union[Unset, None, RestApiPlanSimphonyReadMode] = UNSET,
) -> Optional[Union[Any, SimphonyPlan]]:
    r"""Retrieve a plan timeline for Simphony subsystem

     Restricts the returned queries by filtering against a **body** query parameter in the URL.
    The **body** expected value is the JSON string corresponding to the following structure:
    * start: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * end: the date formatted as ISO8601 in UTC scale (2030-07-05T01:44:47Z)
    * mode: \"strict\" | \"open\" optional: \"open\" Includes the segments partially included in the
    period

    Args:
        id (str):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
        mode (Union[Unset, None, RestApiPlanSimphonyReadMode]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SimphonyPlan]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            start=start,
            end=end,
            mode=mode,
        )
    ).parsed
