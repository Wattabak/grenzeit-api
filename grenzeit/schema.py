from tortoise import fields
from tortoise.models import Model


class MetaDataMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class User(Model, MetaDataMixin):
    pk = fields.IntField(pk=True, unique=True)
    id = fields.UUIDField()
    username = fields.CharField(40, null=False, )
    password = fields.CharField(120, null=False, )
    email = fields.CharField(20, required=False)
    is_active = fields.BooleanField(default=False)

    class Meta:
        table = "user"


class Country(Model):
    pass
