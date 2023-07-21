# Folder structure doesn't allow 'import readrides'

import csv
from collections import Counter, defaultdict
from io import TextIOWrapper
from operator import itemgetter
from pprint import pprint

from loguru import logger
from two_1_readrides import read_into_dictionaries

import tracemalloc

def check_reading_dicts_memory():
    tracemalloc.start()
    with open("Data/ctabus.csv") as f:
        rows = read_into_dictionaries(f)
        route22_riders = [row for row in rows if row["route"] == "22"]
        print(max(route22_riders, key=lambda row: row['rides']))
    dict_mem_use = tracemalloc.get_traced_memory()
    pprint([x/1000000 for x in dict_mem_use])
    tracemalloc.stop()

def check_iterator_memory():
    tracemalloc.start()
    with open("Data/ctabus.csv") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = (dict(zip(headers, row)) for row in reader)
        route22_riders = (row for row in rows if row["route"] == "22")
        print(max(route22_riders, key=lambda row: int(row['rides'])))
    iter_mem_use = tracemalloc.get_traced_memory()
    pprint([x/1000000 for x in iter_mem_use])
    tracemalloc.stop()

check_reading_dicts_memory()
check_iterator_memory()