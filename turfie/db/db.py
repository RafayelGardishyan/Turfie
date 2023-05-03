from tortoise import Tortoise, run_async

from .models import set_config

async def init(config):
    set_config(config)
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['turfie.db.models']}
    )
    await Tortoise.generate_schemas()