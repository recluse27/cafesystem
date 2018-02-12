import asyncio

from .seed_database import main


def seed_database():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(filename="fixtures.bson")
    )
