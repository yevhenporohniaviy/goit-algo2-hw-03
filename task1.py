import networkx as nx
import pandas as pd
from networkx.algorithms.flow import edmonds_karp

# Створення графа для логістичної мережі
G = nx.DiGraph()

# Визначення вузлів
terminals = ['Термінал 1', 'Термінал 2']
warehouses = ['Склад 1', 'Склад 2', 'Склад 3', 'Склад 4']
shops = [f'Магазин {i}' for i in range(1, 15)]

# Додавання ребер з пропускною здатністю (згідно з описом)
edges = [
    ('Термінал 1', 'Склад 1', 25),
    ('Термінал 1', 'Склад 2', 20),
    ('Термінал 1', 'Склад 3', 15),
    ('Термінал 2', 'Склад 3', 15),
    ('Термінал 2', 'Склад 4', 30),
    ('Термінал 2', 'Склад 2', 10),
    ('Склад 1', 'Магазин 1', 15),
    ('Склад 1', 'Магазин 2', 10),
    ('Склад 1', 'Магазин 3', 20),
    ('Склад 2', 'Магазин 4', 15),
    ('Склад 2', 'Магазин 5', 10),
    ('Склад 2', 'Магазин 6', 25),
    ('Склад 3', 'Магазин 7', 20),
    ('Склад 3', 'Магазин 8', 15),
    ('Склад 3', 'Магазин 9', 10),
    ('Склад 4', 'Магазин 10', 20),
    ('Склад 4', 'Магазин 11', 10),
    ('Склад 4', 'Магазин 12', 15),
    ('Склад 4', 'Магазин 13', 5),
    ('Склад 4', 'Магазин 14', 10),
]

# Додавання ребер до графа
G.add_weighted_edges_from(edges, weight='capacity')

# Додаємо штучні джерело та стік для коректної роботи алгоритму
G.add_edge('Джерело', 'Термінал 1', capacity=float('inf'))
G.add_edge('Джерело', 'Термінал 2', capacity=float('inf'))
for shop in shops:
    G.add_edge(shop, 'Сток', capacity=float('inf'))

# Запуск алгоритму Едмондса-Карпа для обчислення максимального потоку
flow_value, flow_dict = nx.maximum_flow(G, 'Джерело', 'Сток', flow_func=edmonds_karp)

# Формування таблиці результатів
rows = []
for terminal in terminals:
    for warehouse in flow_dict[terminal]:
        for shop in flow_dict[warehouse]:
            if flow_dict[warehouse][shop] > 0:
                rows.append({
                    'Термінал': terminal,
                    'Магазин': shop,
                    'Фактичний Потік (одиниць)': flow_dict[warehouse][shop]
                })

df_results = pd.DataFrame(rows)
print(df_results)

# Збереження у CSV
df_results.to_csv('logistic_results.csv', index=False)

# Вивід загального потоку
print(f'\nЗагальний максимальний потік: {flow_value}')
print('Результати збережено у logistic_results.csv')

