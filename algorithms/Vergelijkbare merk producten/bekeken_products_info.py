from algorithms.utils import connect_to_db as connect
con = connect()
cur = con.cursor()

def bekeken_products_info(profiel_id):
    bekeken_products_info_query = f"""
            SELECT viewed_before.id, brand, category, sub_category, sub_sub_category
            FROM viewed_before
            INNER JOIN products on viewed_before.id = products.id
            WHERE profile_id = '{profiel_id}'
            """
    cur.execute(bekeken_products_info_query)
    bekeken_products_info = cur.fetchall()
    similar_products_info_query = f"""
            SELECT similars.id, brand, category, sub_category, sub_sub_category
            FROM similars
            INNER JOIN products on similars.id = products.id
            WHERE profile_id = '{profiel_id}'"""

    cur.execute(similar_products_info_query)
    similar_products_info = cur.fetchall()
    return bekeken_products_info, similar_products_info

if __name__ == '__main__':
    print(bekeken_products_info('5a393eceed295900010386a8'))