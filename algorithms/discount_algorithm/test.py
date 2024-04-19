import algortihm_discount
from algorithms.utils import connect_to_db as connect
import time

start_time = time.time()


def get_correct_query(max_profiles=10000):
    if max_profiles > 2081649:
        max_profiles = 2081649
    con = connect()
    cur = con.cursor()
    # Query to get similar items
    similar_query = f"""
                    select * from profiles
                """
    cur.execute(similar_query)
    similar_values = cur.fetchall()
    return similar_values[:max_profiles]


def check_runtime(runtime):
    if runtime > 3600:
        print(f"'Hours = {int(runtime // 3600)} and Minutes = {int((runtime % 3600) // 60)} and Seconds = {int(runtime % 60)}'", end=" ")
    elif runtime > 60:
        print(f"'Minutes = {int(runtime // 60)} and Seconds = {int(runtime % 60)}'", end=" ")
    else:
        print(f"'Seconds = {int(runtime)}'", end=" ")

def runtime_heipetetikal(runtime, length, interval=[100, 10000, 100000, 1000000, 2081649]):
    if length > 1:
        run_time_per_item = runtime / length
        print("With the same runtime speed, it will take:")
        for i in interval:
            check_runtime(run_time_per_item * i)
            print(f" For {i} profiles")

def check_how_far(here, togo):
    # Probably not the most efficient way to do this, but it works
    interval_list = []
    for i in range(0, togo, int(togo/10)):
        interval_list.append(int(i))

    if here in interval_list:
        runtime = time.time() - start_time
        leftover = [togo-here]
        print(f"\nCurrently at {here} out of {togo}")
        runtime_heipetetikal(runtime, here, interval=leftover)
    pass


def show_data(length=10000):
    len_count = 0
    test_list = get_correct_query(length)
    troubled_list = []
    output_list = []
    for index, i in enumerate(test_list):
        try:
            recommendation = algortihm_discount.get_recommendation(i[0])
            output_list.append(recommendation)
            len_count += len(recommendation)
        except:
            troubled_list.append(i[0])
        finally:
            check_how_far(index, length)
    # Show where the errors are:
    if len(troubled_list) > 0:
        print(
            f"{'-' * 80}\nErrors with: {len(troubled_list)}, id's, thats {(len(troubled_list) / length) * 100} percent with Id's: {troubled_list}\n")
    else:
        print(f"{'-' * 80}\nNo errors found\n")

    # Shows for reference the first and last 5 items
    print("Eerste 5:", output_list[:5], "\nLaatste 5:", output_list[-5:])

    average_len = len_count / len(test_list)
    max_len = min(len(i) for i in output_list)
    min_len = max(len(i) for i in output_list)
    len_sort = {}
    for i in output_list:
        if len(i) in len_sort:
            len_sort[len(i)] += 1
        else:
            len_sort[len(i)] = 1
    print("Max length:", max_len, "\nMin length:", min_len, "\nAverage length:", average_len, "\n")

    sorted_list_asc = sorted(len_sort.keys())
    for i in sorted_list_asc:
        print(f"Length: {i} - Amount: {len_sort[i]}")
    print(f"This tells us that: {(len_sort[0] / len(output_list))*100}% of the profiles won't return a recommendation due to no output.\n ________________________________________________________________________________________\n")

    # Returns the runtime duration (Just a fun addition)
    runtime = time.time() - start_time
    runtime_heipetetikal(runtime, length)


if __name__ == '__main__':
    show_data(1000)