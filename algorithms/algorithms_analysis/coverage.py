import pymongo, pprint, time, random
from tqdm import tqdm
from algorithms.simple_algorithm.algorithm_popularity import PopularityAlgorithm
from algorithms.similar_brand_algorithm.algorithm_similiar import SimilarBrand
from algorithms.utils import time_function, connect_to_db
from algorithms.similar_costumer_products_algorithm.most_comparable_products import most_comparable_products

class Coverage:

    def __init__(self, count):
        self.db = pymongo.MongoClient("mongodb://localhost:27017/")["huwebshop"]
        self.pop_app = PopularityAlgorithm()
        self.sim_app = SimilarBrand()
        self.cur = connect_to_db().cursor()
        self.count = count

    def get_all_keys(self, d):
        keys = []
        for k, v in d.items():
            if k != "_count" and k != "_id":
                keys.append(k)
            if isinstance(v, dict):
                keys.extend(self.get_all_keys(v))
        return keys

    def all_possible_cats(self):
        category_index = self.db["category_index"]
        cats_index = category_index.find_one()

        cats = []
        for cat in cats_index:
            if cat != "_count" and cat != "_id":
                cats.append((cat, None))
                for sub_cat in cats_index[cat]:
                    if sub_cat != "_count" and sub_cat != "_id":
                        cats.append((cat, sub_cat))

        return cats

    def get_keys(self):
        # Get products data
        category_index = self.db["categoryindex"]
        cats_index = category_index.find_one()

        return self.get_all_keys(cats_index)

    @staticmethod
    def format_product(p: dict) -> tuple:
        brand = p.get("brand", None)
        cat = p.get("category", None)
        sub_cat = p.get("sub_category", None)
        sub_sub_cat = p.get("sub_sub_category", None)
        if isinstance(cat, list):
            cat = cat[0]

        return p["_id"], brand, cat, sub_cat, sub_sub_cat

    def format_all_products(self):
        """ This function retrieves all the product IDs"""
        prods = self.db["products"].find()
        return [self.format_product(p) for p in prods]

    def product_ids(self):
        prods = self.db["products"].find()
        return [p["_id"] for p in prods]

    def format_all_profiles(self):
        """ This function retrieves all the profile IDs"""
        prof = self.db["profiles"].find()
        return [p["_id"] for p in prof]

    def create_list(self, prod_ids) -> tuple:
        return random.choices(prod_ids, k=random.randint(1, 15))

    def create_shopping_lists(self):
        prod_ids = self.product_ids()
        amount_lists = 1 * 10**4

        print(f"Creating {format(amount_lists, '_d')} of random shopping carts\n")
        items = [self.create_list(prod_ids) for _ in tqdm(range(amount_lists), colour="white")]
        return items

    def calc_coverage(self, func, data, *args):
        full_coverage = int(len(data) * self.count)
        returned_ids = []
        for prod in tqdm(data, colour="white"):
            returned_ids.append(len(func(prod, *args)))

        print(f"amount of IDs returned similar algorithm: {sum(returned_ids)}\n"
              f"amount of possible IDs that can be returned: {full_coverage}")
        coverage_pop = round((sum(returned_ids) / full_coverage * 100), 2)
        print(f"similar algorithm covers {coverage_pop}% of all possibilities")

    def main(self):
        # Measure time for self.pop_app.popularity_algorithm
        start_time = time.time()
        self.calc_coverage(self.pop_app.popularity_algorithm,
                           self.all_possible_cats(),
                           self.cur, self.count)
        end_time = time.time()
        print(f"Execution time for popularity algorithm: {round(end_time - start_time,2)}s\n")

        # Measure time for self.sim_app.similar_brand
        start_time = time.time()
        self.calc_coverage(self.sim_app.similar_brand,
                           self.format_all_products(),
                           self.cur, self.count)
        end_time = time.time()
        print(f"Execution time for similar brand algorithm: {round(end_time - start_time, 2)}s\n")

        # Measure time for shopping cart
        start_time = time.time()
        self.calc_coverage(most_comparable_products,
                           self.create_shopping_lists(),
                           self.cur)
        end_time = time.time()
        print(f"Execution time for discount algorithm: {round(end_time - start_time, 2)}s")


if __name__ == '__main__':
    app = Coverage(4)
    # ids = app.format_all_profiles()
    # pprint.pp(ids)
    # ids = time_function(app.format_all_products)
    # pprint.pp(ids)

    # coverages tests
    app.main()
    # app.create_shopping_lists()
    # profiles check without data check = 20.98s
    # profiles check  with check = 17.5s

    # 33.88 % of the time the similar algorithm gets a recommendation for a similar brand