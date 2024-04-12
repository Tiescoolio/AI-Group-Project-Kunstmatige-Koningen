from algorithms.utils import connect_to_db as connect
con = connect()
cur = con.cursor()

def producten_van_profiel(profiel_id):
    products_bij_profiel_id = f"""
        SELECT id FROM sessions_products
        INNER JOIN sessions ON sessions_buid = buid
        WHERE profile_id = '{profiel_id}';
    """
    cur.execute(products_bij_profiel_id)
    lijst = [id[0] for id in cur.fetchall()]
    return lijst
if __name__ == '__main__':
    print(producten_van_profiel('5a393d68ed295900010384ca'))
