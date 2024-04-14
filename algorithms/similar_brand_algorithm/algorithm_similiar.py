import pprint


class SimilarBrand:
    query_brand = """
    SELECT id, brand, category, sub_category, sub_sub_category FROM products WHERE brand = %s
    AND category = %s AND sub_category = %s LIMIT %s"""

    query_no_brand = """
    SELECT id, brand, category, sub_category, sub_sub_category FROM products
    WHERE category = %s AND sub_category = %s AND sub_sub_category != %s LIMIT %s"""

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
        """
            Retrieves similar products based on brand and category/subcategories.

            Args:
                prod_data (tuple): Tuple containing product data (prod_id, brand, cat, sub_cat, sub_sub_cat).
                shopping_cart: Shopping cart data (not used in this function).
                cursor: Cursor object for database query execution.
                count (int): Number of similar products to retrieve.

            Returns:
                tuple: Tuple containing the IDs of similar products.
            """
        # Unpack product data
        prod_id, brand, cat, sub_cat, sub_sub_cat = prod_data

        # Execute query to find similar products based on brand and category
        cursor.execute(self.query_brand, (brand, cat, sub_cat, count * 100))
        # Fetch all similar products
        similar_prods = cursor.fetchall()
        pprint.pp(similar_prods)
        # Extract product IDs from similar products
        prod_ids = [prod[0] for prod in similar_prods]

        # Check if there are other similar products based on brand
        if len(prod_ids) < count:
            # If there are not enough similar products, execute query to find additional products based on categories
            cursor.execute(self.query_no_brand, (cat, sub_cat, sub_sub_cat, count))
            similar_prods_no_brand = cursor.fetchall()
            pprint.pp(similar_prods_no_brand)
            for prod in similar_prods_no_brand:
                # Check if enough products have been collected
                if len(prod_ids) >= count:
                    pprint.pp(prod_ids)
                    return tuple(prod_ids)
                prod_ids.append(prod[0])

        # Print similar product IDs (for debugging or logging)
        pprint.pp(prod_ids)

        # Return tuple of product IDs
        return tuple(prod_ids)