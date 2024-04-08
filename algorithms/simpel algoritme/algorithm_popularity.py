import pprint


class PopularityAlgorithm:
    def __init__(self, count, cursor, cats):
        self.count = count
        self.cursor = cursor
        self.cats = cats
    def get_correct_query(self, category, sub_category):
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

    def format_page_path_cat(self) -> tuple:
        """Function to format the given page path into their separate categories."""
        page_path = page_path.replace("producten/", "")[:-1]
        cats = page_path.split("/")

        # category = self.cat_decoded[cats[0]]
        print(cats)
        # print(category)
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

    def popularity_algorithm(self) -> tuple:
        """The popularity algorithm, this algorithm could be considered a similar algorithm,
        however for now it will seen as a popular algorithm."""
        category, sub_category = self.format_page_path_cat()

        # Query to get recommended items filtered by categories
        query = self.get_correct_query(category, sub_category)

        # Execute the SQL query with the given value as parameters
        if category and sub_category:
            self.cursor.execute(query, (category, sub_category, self.count))
        else:
            self.cursor.execute(query, (category, self.count))
        print(category, sub_category)

        # Fetch all the rows returned by the query
        ids = self.cursor.fetchall()
        prod_ids = tuple([_id[0] for _id in ids])
        pprint.pprint(prod_ids)
        return prod_ids
