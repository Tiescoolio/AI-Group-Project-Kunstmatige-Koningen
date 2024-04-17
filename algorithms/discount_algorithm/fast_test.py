import algortihm_discount
from algorithms.utils import connect_to_db as connect


def get_correct_query():
    con = connect()
    cur = con.cursor()
    # Query to get similars items
    similars_query = f"""
                    SELECT count(profile_id) FROM (
                    SELECT DISTINCT profile_id, count(combined.id) FROM ( 
                    SELECT * FROM viewed_before
                    UNION ALL 
                    SELECT * FROM similars) as combined
                    INNER JOIN products on combined.id = products.id
                    WHERE aanbiedingen IS NOT NULL
                    GROUP BY profile_id) as profielen 
                    WHERE profielen.count > 1;
                """
    cur.execute(similars_query)
    similars_values = cur.fetchall()
    return similars_values

output_list = get_correct_query()
print(f"Alle profielen waar ie iets bij zou teruggeven: {output_list[0][0]} dat is {(len(output_list) / 2081649)*100}%")

