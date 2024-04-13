import pprint


class PopularityAlgorithm:
    def __init__(self):
        pass

    def get_top_sub_cat(self, data, count, sub_cat) -> tuple:
        prod_ids = []
        _data = []
        for i, prod in enumerate(data):
            prod_id = prod[1]
            # Returns the list if t
            if len(prod_ids) >= count:
                return tuple(prod_ids)
            if prod[4] == sub_cat:
                prod_ids.append(prod_id)
                _data.append(prod_id)

        # If there are not enough popular items with the same sub_cat.
        # Then add the most popular of the same category.
        if len(prod_ids) < count:
            for prod in data:
                prod_id = prod[1]
                if len(prod_ids) >= count:
                    return tuple(prod_ids)

                if prod_id not in prod_ids and prod not in _data:
                    prod_ids.append(prod_id)


    def popularity_algorithm(self, cats, cursor, count) -> tuple:
        """The popularity algorithm, this algorithm could be considered a similar algorithm,
        however for now it will seen as a popular algorithm."""
        cat, sub_cat = cats[0], cats[1]
        # Query to get recommended items filtered by categories

        query_popular_prods = """SELECT COUNT(*) AS count_prod, t1.id, t2.category, t2.sub_category
                FROM sessions_products AS t1
                JOIN products AS t2 ON t1.id = t2.id
                WHERE t2.category = %s
                GROUP BY t1.id, t2.category, t2.sub_category
                ORDER BY count_prod DESC"""

        cursor.execute(query_popular_prods, (cat,))
        rows1 = cursor.fetchall()
        pprint.pprint(rows1)

        cursor.execute("""SELECT products.id FROM products""")
        rows = cursor.fetchall()
        ids = [pid[0] for pid in rows]

        print(self.get_top_sub_cat(rows1, count, sub_cat))
        # Execute the SQL query with the given value as parameters
        # Return random products IDs for testing pages.
        return ('31811', '30984-wit-3942', '31810', '33731')
