
def profile_ids(products: list, cursor) -> tuple:
    """
        Retrieves the 5 profile IDs that have purchased the most products from the products list.

        Args:
            products (list): List of product IDs.
            cursor: Database cursor object for executing SQL queries.

        Returns:
            tuple: A tuple containing a list of profile IDs and the input list of products.
        """
    select_relatable_purchased_products_profiles_query = f"""
    SELECT profile_id, COUNT(profile_id) AS count
    FROM sessions
    INNER JOIN sessions_products ON buid = sessions_buid
    WHERE id IN ({','.join([f"'{product_id}'" for product_id in products])})
    GROUP BY profile_id
    ORDER BY count DESC
    LIMIT 5;
    """

    # Execute the SQL query adn fetch data
    cursor.execute(select_relatable_purchased_products_profiles_query)
    profile_ids = cursor.fetchall()

    # Extract profile IDs from the fetched results
    profiles = [p[0] for p in profile_ids]
    return profiles, products


if __name__ == "__main__":
    print(profile_ids([2036, 8532], None))
