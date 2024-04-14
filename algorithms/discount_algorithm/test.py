import algortihm_discount
from algorithms.utils import connect_to_db as connect
import time

con = connect()
cur = con.cursor()


def get_correct_query():
    # Query to get similars items
    similars_query = f"""
                    select * from profiles
                """
    cur.execute(similars_query)
    similars_values = cur.fetchall()
    return similars_values[:10000]


def show_data():
    len_count = 0
    output_list = []
    test_list = get_correct_query()
    for i in test_list:
        output_list.append(algortihm_discount.get_recommendation(i))
        len_count += len(output_list[-1])

    print("Lengte van de testlijst:", len(test_list))
    print("Eerste 5:", output_list[:5], "\nLaatste 5:", output_list[-5:])
    average_len = len_count / len(test_list)

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


if __name__ == '__main__':
    show_data()
con.close()
