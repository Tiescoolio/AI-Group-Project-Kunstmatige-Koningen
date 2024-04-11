import pprint


class PopularityAlgorithm:
    def __init__(self, count, cursor, cats):
        self.count = count
        self.cursor = cursor
        self.cats = cats

    def get_correct_query(self, cat, sub_cat):
        if cat and sub_cat:
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

    def popularity_algorithm(self, cat, sub_cat) -> tuple:
        """The popularity algorithm, this algorithm could be considered a similar algorithm,
        however for now it will seen as a popular algorithm."""

        # Query to get recommended items filtered by categories
        query = self.get_correct_query(cat, sub_cat)

        # Execute the SQL query with the given value as parameters
        if cat and sub_cat:
            self.cursor.execute(query, (cat, sub_cat, self.count))
        else:
            self.cursor.execute(query, (cat, self.count))
        print(cat, sub_cat)

        # Fetch all the rows returned by the query
        ids = self.cursor.fetchall()
        prod_ids = tuple([_id[0] for _id in ids])
        pprint.pprint(prod_ids)
        return prod_ids
