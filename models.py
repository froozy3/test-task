from datetime import date,datetime
import sqlite3
import csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker, Session
from datetime import date
from typing import Type
import pandas as pd

Base = declarative_base()


# Модель для таблицы Users
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)

    credits: Mapped["Credit"] = relationship("Credit", back_populates="user")

# Модель для таблицы Credits


class Credit(Base):
    __tablename__ = "credits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    issuance_date: Mapped[date] = mapped_column(nullable=False)
    return_date: Mapped[date] = mapped_column(nullable=False)
    actual_return_date: Mapped[date] = mapped_column(nullable=True)
    body: Mapped[float] = mapped_column(nullable=False)
    percent: Mapped[float] = mapped_column(nullable=False)

    user: Mapped[User] = relationship("User", back_populates="credits")
    payments: Mapped["Payment"] = relationship(
        "Payment", back_populates="credit")

# Модель для таблицы Dictionary


class Dictionary(Base):
    __tablename__ = "dictionary"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

# Модель для таблицы Plans


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    period: Mapped[date] = mapped_column(Date, nullable=False)
    sum: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('dictionary.id'), nullable=False)

    category: Mapped[Dictionary] = relationship("Dictionary")

# Модель для таблицы Payments


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


# Example of creating an engine and tables
engine = create_engine('sqlite:///example.db')
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert_csv_to_sqlite(database_path, table_name, csv_path):
    """
    Универсальный метод для добавления данных из CSV-файла в таблицу SQLite.

    :param database_path: Путь к SQLite базе данных.
    :param table_name: Название таблицы, куда будут добавлены данные.
    :param csv_path: Путь к CSV-файлу.
    """
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Получаем список колонок таблицы
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_columns = [column[1] for column in cursor.fetchall()]

        # Открываем CSV-файл
        with open(csv_path, "r", encoding="utf-8") as csv_file:
            # Указываем разделитель '\t' для табуляции
            reader = csv.DictReader(csv_file, delimiter='\t')

            # Проверяем, что колонки CSV соответствуют колонкам таблицы
            csv_columns = reader.fieldnames
            if not set(csv_columns).issubset(set(table_columns)):
                raise ValueError(
                    f"Колонки CSV ({csv_columns}) не соответствуют колонкам таблицы ({table_columns}).")

            # Формируем запрос для вставки
            # Генерация плейсхолдеров для VALUES
            placeholders = ", ".join(["?"] * len(csv_columns))
            query = f"INSERT INTO {table_name} ({', '.join(csv_columns)}) VALUES ({placeholders})"

            # Добавляем данные из CSV в таблицу
            for row in reader:
                values = []
                for column in csv_columns:
                    value = row[column]

                    # Проверка на пустую строку, заменяем на None (NULL)
                    if value.strip() == '':
                        value = None

                    # Проверка, если значение в столбце — дата
                    if isinstance(value, str) and value:
                        try:
                            # Преобразуем строку в дату (если это возможно)
                            # Можно настроить формат на свой вкус, например, '%d.%m.%Y'
                            parsed_date = datetime.strptime(
                                value, '%d.%m.%Y').date()
                            values.append(parsed_date)
                        except ValueError:
                            # Если не удается преобразовать, оставляем как есть
                            values.append(value)
                    else:
                        values.append(value)

                cursor.execute(query, values)

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()
        print(
            f"Данные из {csv_path} успешно добавлены в таблицу {table_name}.")
    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")



def auto(table_name: str):
    insert_csv_to_sqlite(database_path='example.db', table_name=table_name,
                         csv_path=fr"C:\Users\Владик\Downloads\{table_name}.csv")


# auto(table_name='dictionary')


Base.metadata.create_all(engine)
