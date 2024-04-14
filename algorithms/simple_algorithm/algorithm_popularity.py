import pprint
import sys

class PopularityAlgorithm:
    query = """SELECT COUNT(*) AS count_prod, t1.id, t2.category, t2.sub_category
                        FROM sessions_products AS t1
                        JOIN products AS t2 ON t1.id = t2.id
                        WHERE t2.category = %s
                        GROUP BY t1.id, t2.category, t2.sub_category
                        ORDER BY count_prod DESC"""

    def __init__(self):
        self.prod_ids_cache = {}  # Cache for storing retrieved product IDs

    def check_cache(self, cat, sub_cat):
        """ This function returns prod IDs if they are cached"""
        if cat in self.prod_ids_cache:
            if sub_cat is None:
                return self.prod_ids_cache[cat].get("value", False)
            else:
                return self.prod_ids_cache[cat].get(sub_cat, False)
        return False

    def add_to_cache(self, cat, sub_cat, prod_ids):
        """ This function adds product IDs to the cache"""
        if cat and sub_cat is None:
            self.prod_ids_cache[cat] = {"value": prod_ids}
        elif cat and sub_cat:
            if cat not in self.prod_ids_cache.keys():
                self.prod_ids_cache[cat] = {}

            self.prod_ids_cache[cat][sub_cat] = prod_ids

    def get_top_sub_cat(self, data, count, sub_cat) -> tuple:
        """ This function gets the most popular products per for a subcategory,
        if none are found it will return the most popular items for that category"""
        prod_ids = []
        _data = []
        for i, prod in enumerate(data):
            prod_id = prod[1]
            # Returns the list if t
            if len(prod_ids) >= count:
                return tuple(prod_ids)
            if prod[3] == sub_cat:
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
        pprint.pp(self.prod_ids_cache)

        checked_cache = self.check_cache(cat, sub_cat)
        if checked_cache is not False:
            return checked_cache

        # Fetch all products from the given category
        cursor.execute(self.query, (cat,))
        popular_prods = cursor.fetchall()
        print(f"len pop list = {len(popular_prods)}")

        if sub_cat:
            prod_ids = self.get_top_sub_cat(popular_prods, count, sub_cat)
        else:
            # Return the popular products if no sub_cat is given.
            prods = popular_prods[:4]
            prod_ids = tuple([p[1] for p in prods])

        # Adds the product IDs to the cache
        self.add_to_cache(cat, sub_cat, prod_ids)

        print(prod_ids)
        # Execute the SQL query with the given value as parameters
        # Return random products IDs for testing pages.
        return prod_ids
