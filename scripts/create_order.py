from database import get_connection
import sys
def create_order(customer_id, items):

        with get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(("INSERT INTO orders (customer_id, total_amount) VALUES (%s, 0) RETURNING order_id"), (customer_id,))
                    order_id = cur.fetchone()[0]
                    total_amount = 0
                    for product_id, quantity in items:
                        cur.execute(("SELECT price FROM products WHERE product_id = %s FOR UPDATE"), (product_id,))
                        product = cur.fetchone()
                        if not product:
                            raise ValueError(f"Продукт с ID {product_id} не найден")

                        price = product[0]
                        subtotal = price * quantity

                        cur.execute(
                            ("INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)"),
                            (order_id, product_id, quantity, subtotal)
                        )
                        total_amount += subtotal

                    conn.execute(("UPDATE orders SET total_amount = %s WHERE order_id = %s"), (total_amount, order_id))

                conn.commit()
                print(f"Заказ {order_id} успешно создан на сумму {total_amount}")
            except Exception as e:
                conn.rollback()
                print("Ошибка при создании заказа:", e)

if __name__ == '__main__':
    customer_id = int(sys.argv[1])
    items = [(int(sys.argv[i]), int(sys.argv[i+1])) for i in range(2, len(sys.argv), 2)]
    create_order(customer_id, items)