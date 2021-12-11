import csv

with open('../dump/top_cities_2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['rank', 'city', 'population'])
    writer.writerows([
        [1, '上海', 24_150_000],
        [2, 'カラチ', 23_500_000],
        [3, '北京', 21_516_000],
        [4, '北京', 14_722_100],
        [5, 'イスタンブル', 14_160_467],
    ])