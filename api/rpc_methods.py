from time import sleep

from asgiref.sync import async_to_sync, sync_to_async
from modernrpc.core import REQUEST_KEY, ENTRY_POINT_KEY, PROTOCOL_KEY, HANDLER_KEY
from modernrpc.core import rpc_method


@rpc_method(name='add')
def add(a, b, **kwargs):
    """
    a + b
    :param a: int
    :param b: int
    :return: int
    """
    # protocol = kwargs.get(PROTOCOL_KEY)
    # entry_point = kwargs.get(ENTRY_POINT_KEY)
    # handler = kwargs.get(HANDLER_KEY)
    # request = kwargs.get(REQUEST_KEY)
    # TODO async for list request
    sleep(a+b)
    return a+b
