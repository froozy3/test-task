from datetime import date, datetime
import sqlite3
import csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker, Session
from datetime import date
from typing import Type
import pandas as pd

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)

    credits: Mapped["Credit"] = relationship("Credit", back_populates="user")


class Credit(Base):
    __tablename__ = "credits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    issuance_date: Mapped[date] = mapped_column(nullable=False)
    return_date: Mapped[date] = mapped_column(nullable=False)
    actual_return_date: Mapped[date] = mapped_column(nullable=True)
    body: Mapped[float] = mapped_column(nullable=False)
    percent: Mapped[float] = mapped_column(nullable=False)

    user: Mapped[User] = relationship("User", back_populates="credits")
    payments: Mapped["Payment"] = relationship(
        "Payment", back_populates="credit")


class Dictionary(Base):
    __tablename__ = "dictionary"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    period: Mapped[date] = mapped_column(Date, nullable=False)
    sum: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('dictionary.id'), nullable=False)

    category: Mapped[Dictionary] = relationship("Dictionary")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sum: Mapped[float] = mapped_column(nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    credit_id: Mapped[int] = mapped_column(
        ForeignKey('credits.id'), nullable=False)
    type_id: Mapped[int] = mapped_column(
        ForeignKey('dictionary.id'), nullable=False)

    credit: Mapped[Credit] = relationship("Credit", back_populates="payments")
    type: Mapped[Dictionary] = relationship("Dictionary")


engine = create_engine('sqlite:///example.db')
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert_csv_to_sqlite(database_path, table_name, csv_path):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table_name});")
        table_columns = [column[1] for column in cursor.fetchall()]

        with open(csv_path, "r", encoding="utf-8") as csv_file:

            reader = csv.DictReader(csv_file, delimiter='\t')

            csv_columns = reader.fieldnames
            if not set(csv_columns).issubset(set(table_columns)):
                raise ValueError(
                    f"Колонки CSV ({csv_columns}) не соответствуют колонкам таблицы ({table_columns}).")

            placeholders = ", ".join(["?"] * len(csv_columns))
            query = f"INSERT INTO {table_name} ({', '.join(csv_columns)}) VALUES ({placeholders})"

            for row in reader:
                values = []
                for column in csv_columns:
                    value = row[column]

                    if value.strip() == '':
                        value = None

                    if isinstance(value, str) and value:
                        try:

                            parsed_date = datetime.strptime(
                                value, '%d.%m.%Y').date()
                            values.append(parsed_date)
                        except ValueError:
                            values.append(value)
                    else:
                        values.append(value)

                cursor.execute(query, values)

        conn.commit()
        conn.close()
        print(
            f"Data from {csv_path} successfully added into table {table_name}.")
    except sqlite3.Error as e:
        print(f"Error SQLite: {e}")
    except Exception as e:
        print(f"Error: {e}")


Base.metadata.create_all(engine)
