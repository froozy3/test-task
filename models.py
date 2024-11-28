from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker, relationship, validates

DATABASE_URL = "sqlite:///./spy_cat_agency.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class SpyCat(Base):
    __tablename__ = 'cats'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    years_of_experience: Mapped[int] = mapped_column(nullable=False)
    breed: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False, default=100)

    missions = relationship("Mission", back_populates='cat')


class Mission(Base):
    __tablename__ = 'missions'

    id: Mapped[int] = mapped_column(primary_key=True)
    cat_id: Mapped[int] = mapped_column(ForeignKey('cats.id'), nullable=False)
    complete: Mapped[bool] = mapped_column(default=False)

    cat = relationship("SpyCat", back_populates='missions')
    targets = relationship("Target", back_populates='mission')


class Target(Base):
    __tablename__ = 'targets'

    id: Mapped[int] = mapped_column(primary_key=True)
    mission_id: Mapped[int] = mapped_column(ForeignKey('missions.id'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=False)
    complete: Mapped[bool] = mapped_column(default=False)

    mission = relationship("Mission", back_populates="targets")


def is_success_connection():
    try:
        with engine.connect() as connection:
            print("Connected to data base successfully!")
    except Exception as e:
        print(f"Error connection: {e}")


def create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create_table()
# is_success_connection()
