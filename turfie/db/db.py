from .models import Group, User
from tortoise import Tortoise, run_async
from tortoise.expressions import Q


from .models import Turf, set_config

async def init(config):
    set_config(config)
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['turfie.db.models']}
    )
    await Tortoise.generate_schemas()


async def get_turfs_by_user(user):
    return await Turf.filter(for_user=user).all()

async def get_users_by_group(group):
    return await group.users.all()

async def get_groups_by_user(user):
    groups = await Group.all().get()
    if type(groups) == Group:
        groups = [groups]
    
    for group in groups:
        users = await group.users.all()
        if type(users) == User:
            users = [users]
        for quser in users:
            if quser.username != user.username:
                groups.remove(group)

    return groups