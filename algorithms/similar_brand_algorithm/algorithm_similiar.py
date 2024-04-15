import pprint
from algorithms.utils import connect_to_db, time_function

class SimilarBrand:
    query_brand = """
    SELECT DISTINCT ON (sub_sub_category) id, brand, category, sub_category, sub_sub_category 
    FROM products 
    WHERE brand = %s
    AND category = %s 
    AND sub_category = %s 
    AND sub_sub_category != %s 
    LIMIT %s"""

    query_no_brand = """
    SELECT DISTINCT ON (sub_sub_category) id, brand, category, sub_category, sub_sub_category 
    FROM products
    WHERE sub_category = %s
    AND sub_sub_category != %s 
    LIMIT %s"""

    def __init__(self):
        self.prod_ids_cache = {}  # Cache for storing retrieved product IDs

    def check_cache(self, prod_id):
        """ This function returns prod IDs if they are cached"""
        if prod_id in self.prod_ids_cache.keys():
            return self.prod_ids_cache[prod_id]
        return False

    def add_to_cache(self, prod_id, prod_ids):
        """ This function adds product IDs to the cache"""
        self.prod_ids_cache[prod_id] = prod_ids

    def clean_cache(self, shopping_cart):
        pass

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

        # Check if cached data is available
        checked_cache = self.check_cache(prod_id)
        if checked_cache is not False:
            return checked_cache

        # Execute query to find similar products based on brand and category
        cursor.execute(self.query_brand, (brand, cat, sub_cat, sub_sub_cat, count))
        # Fetch all similar products
        similar_prods = cursor.fetchall()
        for prod1 in similar_prods:
            print(prod1, "first query")
        # Extract product IDs from similar products
        prod_ids = [prod[0] for prod in similar_prods]

        # Check if there are other similar products based on brand
        if len(prod_ids) < count:
            # If there are not enough similar products, execute query to find additional products based on categories
            cursor.execute(self.query_no_brand, (sub_cat, sub_sub_cat, int(count - len(prod_ids))))
            similar_prods_no_brand = cursor.fetchall()
            for prod2 in similar_prods_no_brand:
                print(prod2, "second query")
            for prod in similar_prods_no_brand:
                # Check if enough products have been collected
                if len(prod_ids) >= count:
                    pprint.pp(prod_ids)
                    return tuple(prod_ids)
                prod_ids.append(prod[0])

        prod_ids = tuple(prod_ids)
        # Fall back to still recommend products if the rec alg lacks data
        # if brand is None or sub_cat is None;
            # fall_back(cats, cursor, len(prod_ids), count)

        # Adds the product IDs to the cache
        self.add_to_cache(prod_id, prod_ids)
        print(self.prod_ids_cache)
        # Print similar product IDs (for debugging or logging)
        pprint.pp(prod_ids)

        # Return tuple of product IDs
        return prod_ids


if __name__ == '__main__':
    data = ("21858", "At Home", "Huishouden", "Wassen en schoonmaken", "Afwasmiddel")
    data2 = ("21822", "At Home", "Huishouden", "Wassen en schoonmaken", "Afwasmiddel")
    app = SimilarBrand()
    app.add_to_cache("hello", "ass",)
    with (connect_to_db() as conn, conn.cursor() as cursor):
        ids = time_function(app.similar_brand, data, [None], cursor, 4)

    print(app.prod_ids_cache)
