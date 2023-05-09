from tortoise import Tortoise
from .models import set_config

async def init(config):
    set_config(config)
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['turfie.db.models']}
    )
    # await Tortoise._drop_databases()
    await Tortoise.generate_schemas()