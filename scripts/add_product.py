import sys
from database import get_connection


def add_product(name, price):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO products (product_name, price) VALUES (%s, %s) RETURNING product_id", (name, price))
                product_id = cur.fetchone()[0]

            conn.commit()
            print(f"Продукт {name} успешно добавлен с ID {product_id} и ценой {price}")

    except Exception as e:
        conn.rollback()
        print("Ошибка при добавлении продукта:", e)


if __name__ == "__main__":
    name = sys.argv[1]
    price = float(sys.argv[2])
    add_product(name, price)