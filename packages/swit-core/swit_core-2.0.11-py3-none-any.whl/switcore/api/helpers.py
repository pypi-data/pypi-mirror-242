import inspect
from switcore.api.channel.schemas import Channel
from switcore.api.workspace.schemas import Workspace


def sort_by_name(func):
    async def async_wrapper(*args, **kwargs):
        arr: list[Workspace | Channel] = func(*args, **kwargs)
        if len(arr) > 0:
            assert hasattr(arr[0], "name"), "object has no name attribute!!"
            arr.sort(key=lambda element: getattr(element, "name"))
        return arr

    async def sync_wrapper(*args, **kwargs):
        arr: list[Workspace | Channel] = await func(*args, **kwargs)
        if len(arr) > 0:
            assert hasattr(arr[0], "name"), "object has no name attribute!!"
            arr.sort(key=lambda element: getattr(element, "name"))
        return arr

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
