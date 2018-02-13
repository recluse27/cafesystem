from bson import ObjectId
from sanic.exceptions import InvalidUsage, Forbidden

from app.models import CafeEmployeeDocument, OrderDocument, ProductDocument


def require_json(func):
    async def wrapped(self, request, **kwargs):
        if request.json is None:
            raise InvalidUsage('Data is not provided.')
        return await func(self, request, **kwargs)

    return wrapped


def check_user(func):
    async def wrapped(self, request, **kwargs):
        token = request.headers.get("token")
        if not token:
            raise InvalidUsage(message='Token is not provided.')

        employee = await CafeEmployeeDocument.find_one({"token": token})
        if not employee:
            raise InvalidUsage(message='Invalid token provided.')
        return await func(self, request, user=employee, **kwargs)

    return wrapped


async def check_user_cafe(user, order_id):
    order = await OrderDocument.find_one({"_id": ObjectId(order_id)})
    if order.cafe != user.cafe:
        raise Forbidden(message="You don't have access to this order.")
    return order


async def make_order_with_products(order_data):
    products = []
    for product_id in order_data.get('products'):
        product = await ProductDocument.find_one({"_id": ObjectId(product_id)})
        if product:
            products.append(product.dump())
    order_data['products'] = products
    return order_data


async def find_document_by_field(document, field_name, field_value):
    pass