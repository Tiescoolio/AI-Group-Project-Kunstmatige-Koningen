from algorithms.utils import connect_to_db as connect
from relatable_profile_ids import vergelijkbare_profiel_ids as profile_ids
con = connect()
cur = con.cursor()

def most_comparable_products(profile_id):
    profielen, producten = profile_ids(profile_id)
    most_comparable_products_query = f"""
        SELECT id, SUM(count) as total_count
        FROM (
            SELECT id, COUNT(id) as count
            FROM sessions_products
            INNER JOIN sessions ON sessions_buid = buid
            WHERE profile_id IN ({','.join([f"'{profiel_id}'" for profiel_id in profielen])})
            AND id NOT IN ({','.join([f"'{product}'" for product in producten])})
            GROUP BY id, profile_id
        )
        GROUP BY id
        ORDER BY total_count DESC
        LIMIT 4;
    """

    cur.execute(most_comparable_products_query)
    most_purchased_products = cur.fetchall()

    recommended_products = []

    for rij in most_purchased_products:
        recommended_products.append(rij[0])
    return recommended_products
if __name__ == "__main__":
    print(most_comparable_products('5a393d68ed295900010384ca'))
cur.close()
con.close()