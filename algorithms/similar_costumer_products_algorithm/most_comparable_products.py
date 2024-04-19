from algorithms.similar_costumer_products_algorithm.relatable_profile_ids import profile_ids


def most_comparable_products(products, cursor):
    """
        Retrieves the most comparable products based on the purchasing behavior of similar profiles.

        Args:
            products (list): List of product IDs.
            cursor: Database cursor object for executing SQL queries.

        Returns:
            tuple: A tuple containing a list of recommended product IDs.
    """
    profiles, products = profile_ids(products, cursor)

    # If there are no profiles, return an empty list
    if len(profiles) <= 0:
        return []

    # Construct the SQL query to find the most comparable products
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

    # Execute the SQL query and fetch the results
    cursor.execute(most_comparable_products_query)
    most_purchased_products = cursor.fetchall()

    # Extract recommended product IDs from the fetched results
    recommended_products = [r[0] for r in most_purchased_products]
    return recommended_products
