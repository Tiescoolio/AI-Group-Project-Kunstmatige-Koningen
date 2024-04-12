from algorithms.utils import connect_to_db as connect
from relatable_profile_ids import vergelijkbare_profiel_ids as profiel_ids
con = connect()
cur = con.cursor()

def meest_vergelijkbare_producten(profiel_id):
    profielen, producten = profiel_ids(profiel_id)
    meest_vergelijkbare_producten = f"""
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

    cur.execute(meest_vergelijkbare_producten)
    meest_gekochte_producten = cur.fetchall()

    aanbevolen_producten = []

    for rij in meest_gekochte_producten:
        aanbevolen_producten.append(rij[0])
    return aanbevolen_producten
if __name__ == "__main__":
    meest_vergelijkbare_producten('5a393d68ed295900010384ca')
cur.close()
con.close()