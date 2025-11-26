# from flask import current_app

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:23306/{db_name}?charset=utf8'.format(**{
#     'user': 'sksk_ko',
#     'password': 'Ka83hH36',
#     'host': '127.0.0.1',
#     'db_name': 'sksk_ko'
# }))
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))

# Base = declarative_base()
# Base.query = db_session.query_property()

# def init_db():
#     import sksk_app.models
#     Base.metadata.create_all(bind=engine)