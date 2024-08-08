from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings


# SQLACLHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'
SQLACLHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLACLHEMY_DATABASE_URL = 'postgresql://postgres:Ironman0906@localhost:5432/fastapi-database'

print(SQLACLHEMY_DATABASE_URL)

engine = create_engine(SQLACLHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()