from datetime import datetime
from sql_connection import get_sql_connection

def delete_order(connection, order_id):
    cursor = connection.cursor()
    query = ("DELETE FROM orders where order_id=" + str(order_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid