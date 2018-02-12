import asyncio
from app import app, config, models
from app.routes import add_routes

if __name__ == "__main__":
    app.config.from_object(config)
    add_routes(app)
    server = app.create_server(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(models.create_indexes())
    loop.run_until_complete(server)
    loop.run_forever()
