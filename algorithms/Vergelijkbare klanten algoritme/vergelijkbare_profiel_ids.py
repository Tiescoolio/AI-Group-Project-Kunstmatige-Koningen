from algorithms.utils import connect_to_db as connect

con = connect()

cur = con.cursor()

producten = ['26085', '29438', '8533'] #voorbeeld producten

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

rows = cur.fetchall()

profielen = []
print("Top drie profiel IDs met de hoogste count over alle producten:")
for row in rows:
    print(f"Profiel ID: {row[0]}, aantal: {row[1]}")
    profielen.append(row[0])

cur.close()
con.close()