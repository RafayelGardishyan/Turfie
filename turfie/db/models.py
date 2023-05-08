import json
from typing import Tuple
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
    
    def get_letter(self):
        return self.username[0].upper()
    
    async def save(self, *args, **kwargs):
        self.password = self.encode_password(self.password)
        await super().save()

    def __str__(self) -> str:
        return self.username

class Group(Model):
    name = fields.CharField(max_length=20, unique=True)
    users = fields.ManyToManyField('models.User', related_name='users')

    def get_slug(self):
        return self.name.lower().replace(' ', '-')
    
    def get_letter(self):
        return self.name[0].upper()

    def __str__(self) -> str:
        return self.name
    
    async def get_groups_by_user(user):
        groups = await Group.all()
        if type(groups) == Group:
            groups = [groups]

        finalgroups = []
        
        for group in groups:
            users = await group.users.all()
            print(users)
            if type(users) == User:
                users = [users]
            for quser in users:
                if quser.username == user.username:
                    finalgroups.append(group)
        return finalgroups

class Turf(Model):
    for_user = fields.ForeignKeyField('models.User', related_name='turf_owner')
    registered_by = fields.ForeignKeyField('models.User', related_name='turf_registered_by')
    group = fields.ForeignKeyField('models.Group', related_name='turf_group')
    reason = fields.CharField(max_length=100)

    async def get_turf_count_by_user(groupid: int, userid: int) -> int:
        group = await Group.get(id=groupid)
        user = await User.get(id=userid)
        return await Turf.filter(group=group, for_user=user).count()

    async def get_user_turf_counts(groupid: int) -> list[Tuple]:
        group = await Group.get(id=groupid)
        users = await group.users.all()
        counts = []
        for user in users:
            counts.append((
                user, await Turf.get_turf_count_by_user(groupid, user.id), user.get_letter()
            ))
        counts.sort(key=lambda x: x[1], reverse=True)
        return counts

    async def get_turf_history(groupid: int) -> list:
        group = await Group.get(id=groupid)
        turfs = await Turf.filter(group=group).order_by('-id').limit(6)
        turf_history = []

        for turf in turfs:
            for_user = await turf.for_user.get()
            registered_by = await turf.registered_by.get()
            turf_history.append({
                'for_user': for_user.username,
                'registered_by': registered_by.username,
                'reason': turf.reason,
            })

        return turf_history
    
    def __str__(self) -> str:
        return f'Turf: {self.for_user} for {self.reason} by {self.registered_by} (Group: {self.group})'
