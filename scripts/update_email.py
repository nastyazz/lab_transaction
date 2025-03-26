import sys
from database import get_connection


def update_email(customer_id, new_email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT email FROM customers WHERE customer_id = %s FOR UPDATE", (customer_id,))
                customer = cur.fetchone()
                if not customer:
                    raise ValueError("Клиент не найден")

                cur.execute("UPDATE customers SET email = %s WHERE customer_id = %s", (new_email, customer_id))

            conn.commit()
            print(f"Email клиента {customer_id} успешно обновлен на {new_email}")

    except Exception as e:
        conn.rollback()
        print("Ошибка при обновлении email:", e)


if __name__ == "__main__":
    customer_id = int(sys.argv[1])
    new_email = sys.argv[2]
    update_email(customer_id, new_email)