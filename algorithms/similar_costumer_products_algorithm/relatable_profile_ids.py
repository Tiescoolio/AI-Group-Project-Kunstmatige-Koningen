
def profile_ids(products, cursor):
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

    cursor.execute(select_relatable_purchased_products_profiles_query)
    profile_ids = cursor.fetchall()

    profiles = []
    for profile in profile_ids:
        profiles.append(profile[0])
    return profiles, products


if __name__ == "__main__":
    print(profile_ids([2036,8532]))
