import unittest
import timeit
from simple_algorithm.algorithm_popularity import PopularityAlgorithm  # Import the PopularityAlgorithm class from your module

class TestPopularityAlgorithm(unittest.TestCase):
    def setUp(self):
        # Initialize necessary objects for testing
        self.algorithm = PopularityAlgorithm()
        self.cursor = None  # Initialize your cursor object for database query execution

    def test_popularity_algorithm(self):
        # Define your test case here
        cats = ("category_name", "subcategory_name")  # Example category and subcategory
        count = 5  # Example number of popular products to retrieve
        expected_result = ()  # Define your expected result here based on your algorithm's logic

        # Measure the execution time of the algorithm
        execution_time = timeit.timeit(lambda: self.algorithm.popularity_algorithm(cats, self.cursor, count), number=1)

        # Assert statements to check if the algorithm produces the expected result
        result = self.algorithm.popularity_algorithm(cats, self.cursor, count)
        self.assertEqual(result, expected_result)
        print("Execution time:", execution_time)

if __name__ == '__main__':
    unittest.main()
