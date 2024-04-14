# kijkt naar wat de gebruiker bekeken heeft, en geeft een aanbeveling als er een aanbieding is op die producten.
from algorithms.utils import connect_to_db as connect


def get_correct_query(profiel_id):
    con = connect()
    cur = con.cursor()
    # Query to get similars items
    similars_query = f"""
                    SELECT similars.id, aanbiedingen, selling_price, price_discount FROM similars
                    INNER JOIN products on similars.id = products.id
                    WHERE aanbiedingen IS NOT NULL
                    AND profile_id = '{profiel_id}'
                    ORDER BY aanbiedingen DESC;
                """
    cur.execute(similars_query)
    similars_values = cur.fetchall()

    # Query to get viewed_before items
    viewed_before_query = f"""
                        SELECT viewed_before.id, aanbiedingen, selling_price, price_discount FROM viewed_before
                        INNER JOIN products on viewed_before.id = products.id
                        WHERE aanbiedingen IS NOT NULL
                        AND profile_id = '{profiel_id}'
                        ORDER BY aanbiedingen DESC;
                    """

    cur.execute(viewed_before_query)
    viewed_before_values = cur.fetchall()
    return similars_values, viewed_before_values


# Sort the list based on the percentage discount
def rank_list(values, viewed_before_values, count=4):
    # Add the viewed_before_values to the values list
    for i in viewed_before_values:
        values.append(i)

    percentage_list = []
    for i in values:
        discount_price_per_product = i[1].split(" voor ")
        # Returns the float of the num_items (left side)
        temp = discount_price_per_product[0].replace(",", ".")
        num_items = float(temp)
        # Returns de float of the total_price (right side)
        temp = discount_price_per_product[1].replace(",", ".")
        total_price = float(temp)
        # Calculate the discount price
        discount_price = total_price / num_items  # TEMP
        percentage_discount = (i[2] - (discount_price * 100)) / i[2] * 100
        percentage_list.append({"id": i[0], "percentage_discount": percentage_discount})

    # Sort the list based on the percentage_discount
    sorted_list_descending = sorted(percentage_list, key=lambda x: x["percentage_discount"], reverse=True)

    # At the moment only the id is returned and not the percentage_discount!
    sorted_id_list = []
    for i in sorted_list_descending:
        sorted_id_list.append(i["id"])
    return sorted_id_list[:count]


# Functie om de lijst te sorteren op de beste aanbiedingen
def get_recommendation(profiel_id, count=4):
    # Get the values from the query
    similars_values, viewed_before_values = get_correct_query(profiel_id)
    # Sort the values based on the discount
    recommendation = rank_list(similars_values, viewed_before_values, count)
    return recommendation


if __name__ == '__main__':
    get_recommendation('5a39ac51ed29590001040a30')

# con.close()
