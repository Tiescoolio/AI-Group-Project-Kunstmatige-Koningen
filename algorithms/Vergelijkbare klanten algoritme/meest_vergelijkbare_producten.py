from algorithms.utils import connect_to_db as connect
con = connect()
cur = con.cursor()

profile_ids = ['5a399796a825610001bbece9', '5a09979ea56ac6edb4ef7d32', '59dced61a56ac6edb4da9055', '59dcec84a56ac6edb4d9b0f2', '5a54e3348d11a5e91c0ec8b3']  # Add more profile IDs as needed
producten = ['26085', '30287', "20158"]
meest_vergelijkbare_producten = f"""
    SELECT id, SUM(count) as total_count
    FROM (
        SELECT id, COUNT(id) as count
        FROM sessions_products
        INNER JOIN sessions ON sessions_buid = buid
        WHERE profile_id IN ({','.join([f"'{profile_id}'" for profile_id in profile_ids])})
        AND id NOT IN ({','.join([f"'{product}'" for product in producten])})
        GROUP BY id, profile_id
    )
    GROUP BY id
    ORDER BY total_count DESC
    LIMIT 4;
"""

cur.execute(meest_vergelijkbare_producten)

meest_gekochte_producten = cur.fetchall()

for rij in meest_gekochte_producten:
    print("ID:", rij[0])
    print("Totale Count:", rij[1])

cur.close()
con.close()