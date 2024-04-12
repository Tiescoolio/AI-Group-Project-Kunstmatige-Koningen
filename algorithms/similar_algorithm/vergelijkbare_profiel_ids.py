
from algorithms.utils import connect_to_db as connect
from producten_van_profiel import producten_van_profiel as product_query
con = connect()
cur = con.cursor()

def vergelijkbare_profiel_ids(profiel_id):
    producten = product_query(profiel_id)  # voorbeeld producten

    # pakt de 5 profiel_ids die de meeste producten uit de producten lijst gekocht hebben
    select_vergelijkbare_gekochte_producten_profiel = f"""
    SELECT profile_id, COUNT(profile_id) AS count
    FROM sessions
    INNER JOIN sessions_products ON buid = sessions_buid
    WHERE id IN ({','.join([f"'{product_id}'" for product_id in producten])})
    GROUP BY profile_id
    ORDER BY count DESC
    LIMIT 5;
    """

    cur.execute(select_vergelijkbare_gekochte_producten_profiel)
    profiel_ids = cur.fetchall()

    profielen = []
    for profiel in profiel_ids:
        profielen.append(profiel[0])
    return profielen, producten

if __name__ == "__main__":
    vergelijkbare_profiel_ids('5a393d68ed295900010384ca')
