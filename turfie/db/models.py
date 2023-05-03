import json
from tortoise.models import Model
from tortoise import fields
import hashlib

config = {}

def set_config(new_config):
    global config
    config = new_config

class User(Model):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=64)

    def encode_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        return self.password == self.encode_password(password)
    
    async def save(self, *args, **kwargs):
        self.password = self.encode_password(self.password)
        await super().save()

    def __str__(self) -> str:
        return self.username

class Group(Model):
    name = fields.CharField(max_length=20, unique=True)
    users = fields.ManyToManyField('models.User', related_name='groups')

    def __str__(self) -> str:
        return self.name

class Turf(Model):
    for_user = fields.ForeignKeyField('models.User', related_name='turf_owner')
    registered_by = fields.ForeignKeyField('models.User', related_name='turf_registered_by')
    group = fields.ForeignKeyField('models.Group', related_name='turf_group')
    reason = fields.CharField(max_length=100)
    turf_id = fields.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return f'Turf: {self.for_user} for {self.reason} by {self.registered_by} (Group: {self.group})'
