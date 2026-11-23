import os
from dataclasses import dataclass
from getpass import getpass

import mysql.connector


@dataclass
class Customer:
    customer_id: int
    name: str


def connect():
    user = os.getenv("DB_USER") or input("MySQL user: ").strip()
    password = os.getenv("DB_PASSWORD")
    if password is None:
        password = getpass("MySQL password: ")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=user,
        password=password,
        database="course_storage",
        autocommit=False,
    )


def find_customer(connection, customer_id: int) -> Customer | None:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT customer_id, name FROM customers WHERE customer_id = %s",
            (customer_id,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return Customer(customer_id=row[0], name=row[1])


def main():
    customer_id = 1
    with connect() as connection:
        customer = find_customer(connection, customer_id)
        print(customer)


if __name__ == "__main__":
    main()
