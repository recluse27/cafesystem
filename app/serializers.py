from marshmallow import Schema, fields
from marshmallow.validate import Length


class AuthSerializer(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class CafeEmployeeSerializer(Schema):
    username = fields.String(required=True,
                             validate=[Length(min=6, max=60)])
    password = fields.String(required=True)
    cafe = fields.Field(required=True)
    token = fields.String(required=True)


class PaymentTypeSerializer(Schema):
    name = fields.String(required=True)


class CafeSerializer(Schema):
    name = fields.String(required=True)
    addresses = fields.String(required=True)
    info = fields.String(required=True)
    image_url = fields.String()
    payment_type = fields.Field()


class CategorySerializer(Schema):
    cafe = fields.Field(required=True)
    name = fields.String(required=True, unique=True)
    image_url = fields.String()


class ProductSerializer(Schema):
    category = fields.Field(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    image_url = fields.String()
    available_from = fields.String(required=True)
    available_till = fields.String(required=True)


class OrderSerializer(Schema):
    products = fields.List(fields.Nested(fields.Field))
    user_id = fields.String(required=True)
    cafe = fields.Field(required=True)
    order_time = fields.DateTime(required=True)
    deletion_time = fields.DateTime(default=None)


class PaymentSerializer(Schema):
    order = fields.Field(required=True)
    status = fields.String(required=True)
    deletion_time = fields.DateTime(default=None)
