import pymongo, pprint
from algorithms.simple_algorithm.algorithm_popularity import PopularityAlgorithm
from algorithms.similar_brand_algorithm.algorithm_similiar import SimilarBrand
from algorithms.utils import time_function, connect_to_db


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
        category_index = self.db["categoryindex"]
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

        return p["_id"], brand, cat, sub_cat, sub_sub_cat

    def format_all_products(self):
        """ This function retrieves all the product IDs"""
        prods = self.db["products"].find()
        return [self.format_product(p) for p in prods]

    def calc_cov_popular_app(self):
        all_possible_cats = self.all_possible_cats()
        full_coverage = int(len(all_possible_cats) * self.count)
        returned_ids = []
        for cat in all_possible_cats:
            returned_ids.append(len(self.pop_app.popularity_algorithm(cat, self.cur, self.count)))

        print(f"amount of IDs returned popular algorithm: {sum(returned_ids)}\n"
              f"amount of possible IDs that can be returned: {full_coverage}")
        coverage_pop = round((sum(returned_ids) / full_coverage * 100), 2)
        print(f"Popular algorithm covers {coverage_pop}% of all possibilities")

    def calc_cov_similar_app(self):
        products_data = self.format_all_products()
        full_coverage = int(len(products_data) * self.count)
        returned_ids = []
        for prod in products_data:
            returned_ids.append(len(self.sim_app.similar_brand(prod, self.cur, self.count)))

        print(f"amount of IDs returned similar algorithm: {sum(returned_ids)}\n"
              f"amount of possible IDs that can be returned: {full_coverage}")
        coverage_pop = round((sum(returned_ids) / full_coverage * 100), 2)
        print(f"similar algorithm covers {coverage_pop}% of all possibilities")

    def speed_sessions(self):
        sessions = self.db["sessions"].find()
        return [s["_id"] for s in sessions]

    def session_check(self, s: dict) -> bool:
        ids = s.get("order", {}).get("ids")
        if ids is None or ("recommendations" not in s and "order" not in s):
            return False

        return True

    def speed_profiles(self):
        sessions = self.db["profiles"].find()
        return [s["_id"] for s in sessions if self.session_check(s)]


if __name__ == '__main__':
    app = Coverage(4)
    # categories = app.all_possible_cats()
    # pprint.pp(categories)
    # ids = time_function(app.format_all_products)
    # pprint.pp(ids)

    # coverages tests
    # time_function(app.calc_cov_popular_app)  # 2.91s 100% coverage
    # time_function(app.calc_cov_similar_app)  # 18.33s
    ids, time = time_function(app.speed_profiles)
    print(f"Time for looping sessions: {round((time / 1000), 2)}s")

    # profiles check without data check = 20.98s
    # profiles check  with check = 17.5s