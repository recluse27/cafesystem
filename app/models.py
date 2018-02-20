from hashlib import sha256

from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Document, fields, Instance
from umongo.validate import Length

from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
database = client.cafe_system

instance = Instance(database)


@instance.register
class PaymentTypeDocument(Document):
    name = fields.StringField(required=True, unique=True)


@instance.register
class CafeDocument(Document):
    name = fields.StringField(required=True, unique=True)
    addresses = fields.StringField(required=True)
    info = fields.StringField(required=True)
    image_url = fields.StringField()
    payment_type = fields.ObjectIdField(allow_none=True)


@instance.register
class CafeEmployeeDocument(Document):
    username = fields.StringField(required=True, unique=True, validate=[Length(min=6, max=60)])
    password = fields.StringField(required=True)
    cafe = fields.ObjectIdField(required=True)
    token = fields.StringField(required=True)

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('UTF-8')).hexdigest()

    @classmethod
    async def find_user_by_credentials(cls, username, password):
        if not username or not password:
            return None

        hashed_password = cls.hash_password(password)
        return await cls.find_one({'username': username,
                                   'password': hashed_password})


@instance.register
class CategoryDocument(Document):
    cafe = fields.ObjectIdField(required=True)
    name = fields.StringField(required=True)
    image_url = fields.StringField(allow_none=True)


@instance.register
class ProductDocument(Document):
    category = fields.ObjectIdField(required=True)
    name = fields.StringField(required=True)
    description = fields.StringField(required=True)
    price = fields.FloatField(required=True)
    image_url = fields.StringField()
    available_from = fields.StringField(required=True)
    available_till = fields.StringField(required=True)


@instance.register
class OrderDocument(Document):
    products = fields.ListField(fields.ReferenceField(ProductDocument), required=True)
    cafe = fields.ObjectIdField(required=True)
    user_id = fields.StringField(required=True, unique=True)
    order_time = fields.DateTimeField(required=True)
    status = fields.StringField(required=True)
    code = fields.IntegerField(required=True)
    price = fields.FloatField(required=True)
    deletion_time = fields.DateTimeField(allow_none=True)


@instance.register
class PaymentDocument(Document):
    order = fields.ObjectIdField(required=True)
    status = fields.StringField(required=True)
    deletion_time = fields.DateTimeField(allow_none=True)


async def create_indexes():
    """
    Creating unique indexes.
    """
    await CafeEmployeeDocument.collection.create_indexes(CafeEmployeeDocument.opts.indexes)
