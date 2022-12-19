import json
import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
             id_client Integer NOT null,
             id_search Integer NOT null);
             """)
        conn.commit()
        return ("Структура базы данных создана")

def check_form(conn, user_id,searh_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id_search from client 
        WHERE id_client=%s and id_search=%s;
            """, (user_id,searh_id,))
        r = cur.fetchone()
        if r:
            return True
        return False

def add_form(conn, user_id,searh_id):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(id_client, id_search) VALUES( %s, %s);
        """, (user_id,searh_id))
        conn.commit()
        return ("Запись добавлена")


with psycopg2.connect(database="", user="postgres", password="") as conn:
    with conn.cursor() as cur:
        create_db(conn)




