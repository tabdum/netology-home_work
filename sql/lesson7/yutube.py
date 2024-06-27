# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import Session, sessionmaker
# from sqlalchemy import URL, create_engine, text
 
# engine = create_engine(
#     url='postgresql://postgres:25458914@localhost:5432/lesson7',
#     echo=False,
#     # pool_size=5,
#     # max_overflow=10
# )

# with engine.connect() as conn:
#     res = conn.execute(text('SELECT VERSION()'))
#     print(f'{res.first()}')

# from sqlalchemy import Table, Column, Integer, String, MetaData
# metadata_obj = MetaData()
# workers_table = Table(
#     'workers',
#     metadata_obj,
#     Column('id', Integer, primary_key=True),
#     Column('username', String)
# )
