from algorithms.similar_costumer_products_algorithm.relatable_profile_ids import profile_ids
def most_comparable_products(products, cursor):
    profiles, products = profile_ids(products, cursor)
    most_comparable_products_query = f"""
        SELECT id, SUM(count) as total_count
        FROM (
            SELECT id, COUNT(id) as count
            FROM sessions_products
            INNER JOIN sessions ON sessions_buid = buid
            WHERE profile_id IN ({','.join([f"'{profile_id}'" for profile_id in profiles])})
            AND id NOT IN ({','.join([f"'{product}'" for product in products])})
            GROUP BY id, profile_id
        )
        GROUP BY id
        ORDER BY total_count DESC
        LIMIT 4;
    """

    cursor.execute(most_comparable_products_query)
    most_purchased_products = cursor.fetchall()

    recommended_products = []

    for row in most_purchased_products:
        recommended_products.append(row[0])

    return recommended_products
