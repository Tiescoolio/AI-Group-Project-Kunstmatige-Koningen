def get_correct_query(category, sub_category):
    if category and sub_category:
        popular_query = """
                SELECT id
                FROM products as t1
                WHERE t1.category = %s 
                AND t1.sub_category = %s 
                AND t1.recommendable = true
                ORDER BY t1.aanbiedingen IS NOT NULL DESC
                LIMIT %s;
            """
    else:
        popular_query = """
                        SELECT id
                        FROM products as t1
                        WHERE t1.category = %s 
                        AND t1.recommendable = true
                        ORDER BY t1.aanbiedingen IS NOT NULL DESC 
                        LIMIT %s;
                    """
    return popular_query


def format_page_path(page_path: str) -> tuple:
    """Function to format the given page path into their separate categories."""
    page_path = page_path.replace("producten/", "")[:-1]
    cats = page_path.split("/")

    # Formatting categories because huw webshop returns their names differently from MongoDB
    # Please fix !?
    category = cats[0].replace("-en-", " & ").replace("-", " ").replace("make up", "make-up")

    print(category)
    # Check if only the category is provided
    if len(cats) == 1:
        return category, None
    else:
        sub_category = cats[1].replace("-", " ").replace("make up", "make-up")
    return category, sub_category


def popularity_algorithm(cursor, count: int, page_path: str) -> tuple:
    """The popularity algorithm, this algorithm could be considered a similar algorithm,
    however for now it will seen as a popular algorithm."""
    category, sub_category = format_page_path(page_path)

    # Query to get recommended items filtered by categories
    query = get_correct_query(category, sub_category)

    # Execute the SQL query with the given value as parameters
    if category and sub_category:
        cursor.execute(query, (category, sub_category, count))
    else:
        cursor.execute(query, (category, count))
    print(category, sub_category)

    # Fetch all the rows returned by the query
    ids = cursor.fetchall()
    prod_ids = tuple([_id[0] for _id in ids])

    return prod_ids
