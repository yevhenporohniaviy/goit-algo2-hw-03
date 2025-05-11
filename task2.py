import csv
import os
import random
import timeit
from BTrees.OOBTree import OOBTree

tree_by_price = OOBTree()
dictionary = {}

def add_item_to_tree(item_data):
    price = item_data["Price"]
    if price in tree_by_price:
        tree_by_price[price].append(item_data)
    else:
        tree_by_price[price] = [item_data]

def add_item_to_dict(item_id, item_data):
    dictionary[item_id] = item_data

def range_query_tree(min_price, max_price):
    results = []
    for price, items in tree_by_price.items(min_price, max_price):
        results.extend(items)
    return results

def range_query_dict(min_price, max_price):
    return [v for v in dictionary.values() if min_price <= v["Price"] <= max_price]

def generate_demo_csv(filename, num_records=1000):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ID', 'Name', 'Category', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, num_records + 1):
            writer.writerow({
                'ID': i,
                'Name': f'Product {i}',
                'Category': random.choice(['A', 'B', 'C']),
                'Price': round(random.uniform(10, 1000), 2)
            })
    print(f"Файл {filename} успішно створено.")

def load_data(filename):
    if not os.path.exists(filename):
        generate_demo_csv(filename)

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item_id = int(row["ID"])
            item_data = {
                "ID": item_id,
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"])
            }
            add_item_to_tree(item_data)
            add_item_to_dict(item_id, item_data)

def benchmark():
    prices = [random.uniform(10, 1000) for _ in range(100)]
    range_pairs = [(p, p + 50) for p in prices]

    def run_tree_queries():
        return [len(range_query_tree(p1, p2)) for p1, p2 in range_pairs]

    def run_dict_queries():
        return [len(range_query_dict(p1, p2)) for p1, p2 in range_pairs]

    tree_time = timeit.timeit(run_tree_queries, number=1)
    dict_time = timeit.timeit(run_dict_queries, number=1)

    tree_results = run_tree_queries()
    dict_results = run_dict_queries()

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"  Avg items found: {sum(tree_results)/len(tree_results):.2f}")
    print(f"  Min items found: {min(tree_results)}, Max items found: {max(tree_results)}")

    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
    print(f"  Avg items found: {sum(dict_results)/len(dict_results):.2f}")
    print(f"  Min items found: {min(dict_results)}, Max items found: {max(dict_results)}")

if __name__ == "__main__":
    load_data("generated_items_data.csv")
    benchmark()
