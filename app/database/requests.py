from app.database.model import async_session
from app.database.model import User
from sqlalchemy import select


async def db_set_user(tg_id: int, username: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username = username, balance = 0, free_messages = 10))
            await session.commit()

async def db_get_user_id(username):
    async with async_session() as session:
        base = await session.scalar(select(User).where(User.username == username))
        return base.tg_id

async def db_get_balance(tg_id):
    async with async_session() as session:
        base = await session.scalar(select(User).where(User.tg_id == tg_id))
        return base.balance
    
async def db_add_balance(tg_id, amount):
    async with async_session() as session:
        base = await session.scalar(select(User).where(User.tg_id == tg_id))
        balance = base.balance
        base.balance = balance + amount

        session.add(base)

        await session.commit()

async def db_get_free_messages(tg_id):
    async with async_session() as session:
        base = await session.scalar(select(User).where(User.tg_id == tg_id))
        return base.free_messages
    
async def db_add_free_messages(tg_id,amount):
    async with async_session() as session:
        base = await session.scalar(select(User).where(User.tg_id == tg_id))
        free_messages = base.free_messages
        base.free_messages = free_messages + amount

        session.add(base)

        await session.commit()

# async def get_categories():
#     async with async_session() as session:
#         return await session.scalars(select(Category))


# async def get_category_item(category_id):
#     async with async_session() as session:
#         return await session.scalars(select(Item).where(Item.category == category_id))


# async def get_item(item_id):
#     async with async_session() as session:
#         return await session.scalar(select(Item).where(Item.id == item_id))