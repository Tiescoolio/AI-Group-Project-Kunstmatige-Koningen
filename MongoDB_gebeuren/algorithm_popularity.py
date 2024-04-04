import psycopg2
from utils import connect_to_db

def popularity_algorithm(cursor, count, category=None, sub_category=None) -> list:

    orders_select = """SELECT id, COUNT(*) AS aantal
                        FROM ordered           
                        GROUP BY id
                        ORDER BY aantal DESC
                        limit 4"""
    # populairste = cur.fetchall()
    # print(populairste)