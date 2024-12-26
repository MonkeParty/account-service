from app.users.dao import UserDAO


async def get_user_sub_info(id_user: int) -> dict:
    has_sub = await UserDAO.get_has_sub(id_user=id_user)

    if has_sub is None:
        return {
            'has_sub': False
        }

    return {
        'has_sub': has_sub
    }

async def set_sub_for_user(id_user: int) -> dict:
    user = await UserDAO.find_by_id(id_user)

    if user is None:
        return {
            'msg': 'err'
        }

    filter_by = {'id': id_user}
    values = {'has_sub': True}

    await UserDAO.update(
        filter_by,
        **values
    )

    return {
        'msg': 'ok'
    }

async def unsub_user(id_user: int) -> dict:
    user = await UserDAO.find_by_id(id_user)

    if user is None:
        return {
            'msg': 'err'
        }

    filter_by = {'id': id_user}
    values = {'has_sub': False}

    await UserDAO.update(
        filter_by,
        **values
    )

    return {
        'msg': 'ok'
    }