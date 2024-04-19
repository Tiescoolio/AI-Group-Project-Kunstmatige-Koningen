from bekeken_products_info import bekeken_products_info as product_info


def vergelijkbare_merk_producten(profile_id):
    product_id, brand, category, sub_categories, sub_sub_categories = product_info(profile_id)
    vergelijkbare_merk_producten_query = f"""
            SELECT id FROM products
            WHERE id <> '{product_id}'
            AND brand = '{brand}'
            AND category = '{category}'
            AND sub_category = '{sub_categories}'
            AND sub_sub_category IS NOT '{sub_sub_categories}';"""