from app.views import IndexView, LoginView, OrdersView, OrdersByIdView

routes = [{"handler": IndexView, "path": "/"},
          {"handler": LoginView, "path": "/login/"},
          {"handler": OrdersView, "path": "/orders/"},
          {"handler": OrdersByIdView, "path": "/orders/<order_id>/"}]


def add_routes(app):
    for route in routes:
        app.add_route(route.get('handler').as_view(), route.get('path'))
