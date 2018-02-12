import uuid

from sanic.response import json, text
from sanic.exceptions import Forbidden, InvalidUsage
from sanic.views import HTTPMethodView

from app.models import CafeEmployeeDocument, OrderDocument
from app.serializers import AuthSerializer, OrderSerializer
from app.utils import require_json, check_user, crosscheck_user_order


class IndexView(HTTPMethodView):
    async def get(self, request):
        return text("ok")


class LoginView(HTTPMethodView):
    @require_json
    async def post(self, request):
        serialized_user, errors = AuthSerializer().load(request.json)
        if errors:
            raise InvalidUsage(message=f"Wrong data provided: {errors}")
        user = await CafeEmployeeDocument.find_user_by_credentials(**serialized_user)
        if not user:
            raise Forbidden("No user found by provided credentials.")

        user.token = str(uuid.uuid4())
        await user.commit()
        return json({"token": user.token}, status=200)


class OrdersView(HTTPMethodView):
    @check_user
    async def get(self, request, user):
        orders_cursor = OrderDocument.find({"cafe": user.cafe})
        orders = [order.dump() async for order in orders_cursor]
        return json({"orders": orders}, status=200)


class OrdersByIdView(HTTPMethodView):
    @check_user
    async def get(self, request, user, order_id):
        order = await crosscheck_user_order(user, order_id)
        return json({"order": order.dump()}, status=200)

    @require_json
    @check_user
    async def put(self, request, user, order_id):
        order = await crosscheck_user_order(user, order_id)
        serialized_order, errors = OrderSerializer().load(request.json, partial=True)
        if errors:
            raise InvalidUsage(message=f"Wrong data provided: {errors}")
        order.update(serialized_order)
        await order.commit()
        return json({'order': str(order.pk)}, status=200)

    @check_user
    async def delete(self, request, user, order_id):
        order = await crosscheck_user_order(user, order_id)
        await order.delete()
        return json({'order': order_id}, status=200)
