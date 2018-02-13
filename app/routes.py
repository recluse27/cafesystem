from app.views import cafe_views

namespaces = [
    {"name": "/cafe",
     "routes": [{"handler": cafe_views.IndexView, "path": "/"},
                {"handler": cafe_views.LoginView, "path": "/login/"},
                {"handler": cafe_views.OrdersView, "path": "/orders/"},
                {"handler": cafe_views.OrdersByIdView, "path": "/orders/<order_id>/"}]
     }
]


def add_routes(app):
    for namespace in namespaces:
        name = namespace.get('name')
        routes = namespace.get('routes')
        for route in routes:
            app.add_route(route.get('handler').as_view(), f"{name}{route.get('path')}")
