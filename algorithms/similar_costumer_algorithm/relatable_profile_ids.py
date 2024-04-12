from algorithms.utils import connect_to_db as connect
from products_from_profile import products_from_profile
con = connect()
cur = con.cursor()

def vergelijkbare_profiel_ids(profiel_id):
    products = products_from_profile(profiel_id)  # voorbeeld producten

    # pakt de 5 profiel_ids die de meeste producten uit de producten lijst gekocht hebben
    select_relatable_purchased_products_profiles_query = f"""
    SELECT profile_id, COUNT(profile_id) AS count
    FROM sessions
    INNER JOIN sessions_products ON buid = sessions_buid
    WHERE id IN ({','.join([f"'{product_id}'" for product_id in products])})
    GROUP BY profile_id
    ORDER BY count DESC
    LIMIT 5;
    """

    cur.execute(select_relatable_purchased_products_profiles_query)
    profile_ids = cur.fetchall()

    profiles = []
    for profile in profile_ids:
        profiles.append(profile[0])
    return profiles, products

if __name__ == "__main__":
    print(vergelijkbare_profiel_ids('5a393d68ed295900010384ca'))
