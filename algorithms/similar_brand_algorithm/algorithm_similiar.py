import pprint


class SimilarBrand:
    query = """SELECT *
    FROM products 
    WHERE brand = %s
    AND category = %s
    AND sub_category = %s
    AND sub_sub_category != %s"""

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

    def similar_brand(self, prod_data, shopping_cart, cursor, count) -> tuple:
        prod_id, brand, cat, sub_cat, sub_sub_cat = prod_data

        cursor.execute(self.query, (brand, cat, sub_cat))
        rows = cursor.fetchall()
        pprint.pp(rows)
