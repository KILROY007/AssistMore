from sql_connection import get_sql_connection

def login(connection):
    cursor=connection.cursor()
    query=("SELECT user_info.email,username_password")
    cursor.execute(query)
    inf=cursor.fetchone()
    return inf
    