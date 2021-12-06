import json

cities = [
    {'rank': 1, 'city': '上海', 'population': 24_150_000},
    {'rank': 2, 'city': 'カラチ', 'population': 23_500_000},
    {'rank': 3, 'city': '北京', 'population': 21_516_000},
    {'rank': 4, 'city': '天津', 'population': 14_722_100},
    {'rank': 5, 'city': 'イスタンブル', 'population': 14_160_467},
]

print(json.dumps(cities, ensure_ascii=False, indent=2))

with open('dump/top_cities.json', 'w') as f:
    json.dump(cities, f)
