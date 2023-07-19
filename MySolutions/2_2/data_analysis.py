# Folder structure doesn't allow 'import readrides'

import csv
from collections import Counter, defaultdict
from io import TextIOWrapper
from operator import itemgetter
from pprint import pprint

from loguru import logger


def read_into_dictionary(f: TextIOWrapper) -> list[dict]:
    records = []
    rows = csv.reader(f)
    next(rows)  # Skip headers
    for row in rows:
        records.append(
            {"route": row[0], "date": row[1], "daytype": row[2], "rides": int(row[3])}
        )
    return records


def count_unique_routes(data: list[dict]) -> int:
    return len({x["route"] for x in data})


def count_of_riders_on_date(
    data: list[dict], route_to_check: str, date_to_check: str
) -> int:
    return sum(
        [
            x["rides"]
            for x in data
            if x["date"] == date_to_check and x["route"] == route_to_check
        ]
    )


def count_num_riders_per_route(data: list[dict]):
    total_rides_per_route = Counter()
    for row in data:
        total_rides_per_route[row["route"]] += row["rides"]
    return [
        {"Route": x, "Rides": total_rides_per_route[x]} for x in total_rides_per_route
    ]


def calculate_growth_between_years(
    data: list[dict], start_year: int, end_year: int
) -> list[dict]:
    data = group_data_by_route_year(data)
    route_growth = [
        {"route": route, "growth": data[route][end_year] - data[route][start_year]}
        for route in data
    ]
    return sorted(route_growth, key=itemgetter("growth"), reverse=True)


def group_data_by_route_year(data):
    # Nested Default Dict so we can group years by grouped bus routes
    by_route = defaultdict(lambda: defaultdict(int))

    for row in data:
        # Get the Year from the date instead of dealing with DateTime Library
        data_year = int(row["date"].split("/")[2])
        by_route[row["route"]][data_year] += row["rides"]
    return dict(by_route)


if __name__ == "__main__":
    # Row Example:
    # {'date': '06/19/2004', 'daytype': 'A', 'rides': 409, 'route': '40'}
    with open("Data/ctabus.csv") as f:
        data = read_into_dictionary(f)

    # Q1 - How Many Bus Routes exist in Chicago
    logger.info(f"There are {count_unique_routes(data)} unique Bus routes in Chicago")

    # Q2 - How many people rode the number 22 bus on Feb 2, 2011
    #      How about Any day of your choosing?
    date_to_check = "02/02/2011"
    logger.info(
        f"{count_of_riders_on_date(data=data, route_to_check='22', date_to_check=date_to_check)} people took the Number 22 Bus in Chicago on {date_to_check}"
    )

    # Q3 - What is the total number of rides taken on each route?
    rider_report = count_num_riders_per_route(data)
    logger.info(
        f"Here is a report of the total number of riders taken on each of the {len(rider_report)} unique chicago bus routes: "
    )
    pprint(rider_report)

    # Q4 - What 5 Bus Routes had the greates 10 year increase in ridership from 2001-2011
    top_x_routes = 5
    start_year = 2001
    end_year = 2011
    top_routes = calculate_growth_between_years(
        data=data, start_year=start_year, end_year=end_year
    )
    logger.success(
        f"Here are the top {top_x_routes} routes by Growth between {start_year} and {end_year}"
    )
    for x in top_routes[0:5]:
        logger.info(
            f"Route {x['route']} saw a growth of {x['growth']} riders between {start_year} and {end_year}"
        )
