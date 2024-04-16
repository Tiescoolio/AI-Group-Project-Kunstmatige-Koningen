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
    def format_product(self, p: dict) -> tuple:
        brand = p.get("brand", None)
        cat = p.get("category", None)
        sub_cat = p.get("sub_category", None)
        sub_sub_cat = p.get("sub_sub_category", None)

        return p["_id"], brand, cat, sub_cat, sub_sub_cat

    def get_all_ids(self):
        """ This function retrieves all the product IDs"""
        prods = self.db["products"].find()
        return [self.format_product(p) for p in prods]

    def calc_cov_popular_app(self):
        all_possible_cats = self.all_possible_cats()
        full_coverage_pop = int(len(all_possible_cats) * self.count)
        returned_ids = []
        for cat in all_possible_cats:
            returned_ids.append(len(self.pop_app.popularity_algorithm(cat, self.cur, self.count)))

        print(f"amount of IDs returned popular algorithm: {sum(returned_ids)}\n"
              f"amount of possible IDs that can be returned: {full_coverage_pop}")
        coverage_pop = round((sum(returned_ids) / full_coverage_pop * 100), 2)
        print(f"Popular algorithm covers {coverage_pop}% of all possibilities")

    def calc_cov_similar_app(self):
        prod_ids = self.get_all_ids()
        returned_ids = []
        for p_id in prod_ids:
            returned_ids.append(len(self.sim_app.similar_brand(p_id, self.cur, self.count)))


if __name__ == '__main__':
    app = Coverage(4)
    # categories = app.all_possible_cats()
    # pprint.pp(categories)
    ids = time_function(app.get_all_ids)
    pprint.pp(ids)
    # time_function(app.calc_cov_popular_app)
    # time_function(app.calc_cov_similar_app)