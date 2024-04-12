from algorithms.utils import connect_to_db as connect
con = connect()
cur = con.cursor()

def products_from_profile(profile_id):
    products_from_profile_query = f"""
        SELECT id FROM sessions_products
        INNER JOIN sessions ON sessions_buid = buid
        WHERE profile_id = '{profile_id}';
    """
    cur.execute(products_from_profile_query)
    list = [id[0] for id in cur.fetchall()]
    return list
if __name__ == '__main__':
    print(products_from_profile('5a393d68ed295900010384ca'))
