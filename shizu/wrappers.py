from asyncio import iscoroutine, wrap_future
from concurrent.futures import ThreadPoolExecutor
from functools import wraps as _wraps
from inspect import iscoroutinefunction
from types import ModuleType
from typing import Callable


def wrap_function_to_async(function: Callable) -> Callable:
    """Wraps synchronous functions into asynchronous"""

    assert not iscoroutinefunction(function), "The function is already asynchronous!"
    assert not iscoroutine(function), "A function is expected, a coroutine is obtained."

    pool = ThreadPoolExecutor()

    @_wraps(function)
    def wrapped(*args, **kwargs):
        future = pool.submit(function, *args, **kwargs)
        return wrap_future(future)

    return wrapped


class WrapModuleToAsync:
    """Does the same as wrap_function_to_async but wraps whole modules already"""

    def __init__(self, mod: ModuleType):
        for attr in dir(mod):
            item = getattr(mod, attr)
            if (
                callable(item)
                and not iscoroutinefunction(item)
                and not iscoroutine(item)
            ):
                wrapped = wrap_function_to_async(item)
                setattr(self, attr, wrapped)
            else:
                setattr(self, attr, item)
