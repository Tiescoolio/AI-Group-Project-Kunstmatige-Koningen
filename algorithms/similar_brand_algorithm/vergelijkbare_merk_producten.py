from bekeken_products_info import bekeken_products_info as product_info
from algorithms.utils import connect_to_db as connect
con = connect()
cur = con.cursor()

def vergelijkbare_merk_producten(profiel_id):
    id, merk, categorie, sub_categorien, sub_sub_categorien = product_info(profiel_id)
    vergelijkbare_merk_producten_query = f"""
            SELECT id FROM products
            WHERE id <> '{id}'
            AND brand = '{merk}'
            AND category = '{categorie}'
            AND sub_category = '{sub_categorien}'
            AND sub_sub_category IS NOT '{sub_sub_categorien}';"""