import uuid

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, exec_mod_ref: str, resource_id: str, *, name: str, **kwargs):
    func = hub.exec[exec_mod_ref].get

    if "name" in func.signature._parameters:
        kwargs["name"] = name

    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result


async def list_(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
):
    func = hub.exec[exec_mod_ref].list

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    # The return from "list" functions is a dictionary of "resource_id": resource
    # This makes it possible to use access items from the list function in arg_binding by resource_id
    #     instead of the much less meaningful list index.
    # If the "list" function returned a dict, we are done
    if isinstance(result.ret, dict):
        return result

    # Otherwise, "list" returned a literal list, and it needs to be converted into a dict of resource_id:resource
    #     "list" is a -verb synonymous with  "enumerate" -- it is not a reference to a literal python data structure
    acc = {}
    for resource in result["ret"]:
        resource_id = (
            resource.get("resource_id") or f"{resource.get('name')}-{uuid.uuid4()}"
        )
        acc[resource_id] = resource

    result["ret"] = acc
    return result


async def create(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
):
    func = hub.exec[exec_mod_ref].create

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result


async def update(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
):
    func = hub.exec[exec_mod_ref].update

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result


async def delete(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
):
    func = hub.exec[exec_mod_ref].delete

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result
