from mongodb_data.products_data import get_mongo


if __name__ == '__main__':
    results = get_mongo()
    for item in results:
        print(item)