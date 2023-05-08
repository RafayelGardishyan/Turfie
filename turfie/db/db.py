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