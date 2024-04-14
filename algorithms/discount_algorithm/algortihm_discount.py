# kijkt naar wat de gebruiker bekeken heeft, en geeft een aanbeveling als er een aanbieding is op die producten.

from algorithms.utils import connect_to_db as connect

con = connect()
cur = con.cursor()


def get_correct_query(profiel_id):
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

#print(get_recommendation("5a393d68ed295900010384ca"))



# Test the function
# 100 random profile_id's
test_list = ['5a393d68ed295900010384ca', '5a393eceed295900010386a8', '5a393ef6a825610001bb6c51',
             '5a39402ba825610001bb6dc1', '5a3940cea825610001bb6e93', '5a39414ba825610001bb6f3d',
             '5a3941e1ed29590001038ad9', '5a394475ed29590001038e43', '5a394487a825610001bb7348',
             '5a3945b0ed29590001038fea', '5a39484fed2959000103930c', '5a394aa8a825610001bb7aed',
             '5a394ab6a825610001bb7b02', '5a394b1fed29590001039651', '5a394b43a825610001bb7ba5',
             '5a394b78ed295900010396a5', '5a394bebed2959000103972f', '5a394c9fed2959000103980a',
             '5a394ce4a825610001bb7d7b', '5a394d22a825610001bb7dce', '5a394d7da825610001bb7e43',
             '5a394ff7a825610001bb8186', '5a395022a825610001bb81c7', '5a395297a825610001bb8512',
             '5a39530eed2959000103a084', '5a395341ed2959000103a0e0', '5a3953b9ed2959000103a19e',
             '5a39557bed2959000103a409', '5a39567fed2959000103a539', '5a3956dfa825610001bb8b33',
             '5a395850ed2959000103a7f4', '5a3958f3ed2959000103a8d4', '5a395a04ed2959000103aa47',
             '5a395b0ced2959000103abdb', '5a395bb2a825610001bb927e', '5a395bcfed2959000103acdc',
             '5a395cd7a825610001bb9413', '5a395d1aa825610001bb9484', '5a395fc1ed2959000103b24d',
             '5a3960cfa825610001bb9a4e', '5a396289a825610001bb9dbb', '5a3962c2a825610001bb9e1c',
             '5a396308ed2959000103b77a', '5a39636ced2959000103b809', '5a396483ed2959000103b9be',
             '5a396487ed2959000103b9c5', '5a396500ed2959000103ba7e', '5a396522ed2959000103baac',
             '5a396779a825610001bba692', '5a3969f3ed2959000103c2de', '5a396ac7ed2959000103c44a',
             '5a396cfea825610001bbb137', '5a396d94a825610001bbb241', '5a396e36a825610001bbb368',
             '5a396ee0ed2959000103cb30', '5a39710ded2959000103ce9d', '5a39711ced2959000103ceba',
             '5a397129a825610001bbb8b5', '5a397159ed2959000103ceff', '5a3972cbed2959000103d12c',
             '5a397393a825610001bbbcea', '5a397484a825610001bbbe83', '5a3974beed2959000103d439',
             '5a39753bed2959000103d51f', '5a397581a825610001bbc048', '5a3975cbed2959000103d624',
             '5a3975cfed2959000103d62e', '5a39768fa825610001bbc270', '5a3976f8a825610001bbc33c',
             '5a397721a825610001bbc37e', '5a397876ed2959000103da73', '5a3979d4a825610001bbc7bc',
             '5a397bc1a825610001bbca9d', '5a397bd1a825610001bbcab4', '5a397bd4ed2959000103df89',
             '5a397c64a825610001bbcba1', '5a397cb7a825610001bbcc42', '5a397d03a825610001bbccc4',
             '5a397d71a825610001bbcd92', '5a397fa8ed2959000103e547', '5a3982eca825610001bbd607',
             '5a3984d7a825610001bbd949', '5a39855fa825610001bbda0f', '5a3986a7ed2959000103ef62',
             '5a3986e5a825610001bbdc2e', '5a398ae5a825610001bbe134', '5a398da4ed2959000103f795',
             '5a399285a825610001bbe8e1', '5a399534ed2959000103fe46', '5a3996dded2959000103ff95',
             '5a399796a825610001bbece9', '5a39983ea825610001bbed51', '5a399866ed295900010400a3',
             '5a399c52a825610001bbf052', '5a399d37ed2959000104041c', '5a399d9ea825610001bbf161',
             '5a39a469ed295900010407dc', '5a39a76ca825610001bbf5d6', '5a39aa41a825610001bbf69f',
             '5a39ac51ed29590001040a30']

len_count = 0
output_list = []
for i in test_list:
    output_list.append(get_recommendation(i, 100))
    len_count += len(output_list[-1])

print("Eerste 5:", output_list[:5], "\nLaatste 5:", output_list[-5:])
average_len = len_count/len(test_list)

max_len = 0
min_len = 100
len_sort = {}
for i in output_list:
    if len(i) > max_len:
        max_len = len(i)
    if len(i) < min_len:
        min_len = len(i)
    if len(i) in len_sort:
        len_sort[len(i)] += 1
    else:
        len_sort[len(i)] = 1

print("Max length:", max_len, "\nMin length:", min_len, "\nGemiddelde lengte:", average_len)

sorted_list_asc = sorted(len_sort.keys())

for i in sorted_list_asc:
    print(f"Length: {i} - Amount: {len_sort[i]}")

con.close()
