from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite databáza — uloží sa ako súbor space_tours.db v rovnakom priečinku
DATABASE_URL = "sqlite:///./space_tours.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # potrebné pre SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Táto funkcia sa volá pri každom requeste — otvorí a zatvorí spojenie s DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
