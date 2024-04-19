from algorithms.utils import connect_to_db


def get_correct_query(profiel_id, cursor):
    """ This function retrieves similar items and items viewed before with discounts from the database."""

    # Query to get similar items
    similar_prods_query = f"""
                    SELECT similars.id, aanbiedingen, selling_price, price_discount FROM similars
                    INNER JOIN products on similars.id = products.id
                    WHERE aanbiedingen IS NOT NULL
                    AND profile_id = '{profiel_id}'
                    ORDER BY aanbiedingen DESC;
                """
    cursor.execute(similar_prods_query)
    similar_values = cursor.fetchall()

    # Query to get viewed_before items
    viewed_before_query = f"""
                        SELECT viewed_before.id, aanbiedingen, selling_price, price_discount FROM viewed_before
                        INNER JOIN products on viewed_before.id = products.id
                        WHERE aanbiedingen IS NOT NULL
                        AND profile_id = '{profiel_id}'
                        ORDER BY aanbiedingen DESC;
                    """

    cursor.execute(viewed_before_query)
    viewed_before_values = cursor.fetchall()

    return similar_values, viewed_before_values


def rank_list(values, viewed_before_values, count=4):
    """
    Sorts the list based on the percentage discount and user viewing behavior.

    Args:
        values (list): List of similar items with discounts.
        viewed_before_values (list): List of items viewed before with discounts.
        count (int): Number of recommendations to return.

    Returns:
        list: A list of recommended product IDs sorted by the best deals.
    """

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

    # Sort the list based on the percentage_discount variable
    sorted_list_descending = sorted(percentage_list, key=lambda x: x["percentage_discount"], reverse=True)

    # Currently, only the ID is returned, and the percentage discount is not included!
    sorted_id_list = []
    for i in sorted_list_descending:
        sorted_id_list.append(i["id"])
    return sorted_id_list[:count]


def get_recommendation(profiel_id, cursor, count=4):
    """ Function to sort the list based on the best deals."""
    # Get the values from the query
    similar_values, viewed_before_values = get_correct_query(profiel_id, cursor)
    # Sort the values based on the discount
    recommendation = rank_list(similar_values, viewed_before_values, count)
    return recommendation


if __name__ == '__main__':
    # Testing algorithm
    cur = connect_to_db().cursor()
    get_recommendation('5a393d68ed295900010384ca', cur)
