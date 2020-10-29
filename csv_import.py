import csv

from hash_table import HashTable
from location import Location
from package import Package
from datetime import datetime


def get_locations():
    locations = []
    with open("./data/locations.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            locations.append(Location(int(row["id"]), row["name"], row["address"]))
        return locations


def get_distances(locations):
    distances = HashTable()
    with open("./data/distance.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        for rowIndex, row in enumerate(csv_reader):
            distances.set(locations[rowIndex].address, HashTable())
            for distanceIndex, distance in enumerate(row):
                if distance != "" and distance != "0.0":
                    if distances.get(locations[rowIndex].address) is None:
                        distances.set(locations[rowIndex].address, HashTable())
                    inner_hash = distances.get(locations[rowIndex].address)
                    inner_hash.set(locations[distanceIndex].address, float(distance))
    return distances


def convert_deadline_to_datetime(deadline):
    EOD_time = datetime.strptime("17:00:00", "%H:%M:%S").time()
    now = datetime.today()
    if deadline == "EOD":
        return datetime.combine(now, EOD_time)
    deadline_time = datetime.strptime(deadline, "%H:%M:%S").time()
    dt = datetime.combine(now, deadline_time)
    return dt


def parse_notes(note):
    if note == "N/A":
        return False
    return note


def get_packages(locations):
    packages = []
    with open("./data/packages.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            package_location = [
                location for location in locations if location.address == row["address"]
            ][0]
            new_package = Package(
                int(row["id"]),
                package_location,
                convert_deadline_to_datetime(row["deadline"]),
                int(row["mass"]),
                parse_notes(row["notes"]),
            )
            packages.append(new_package)
        return packages


def load_data():
    locations = get_locations()
    return locations, get_distances(locations), get_packages(locations)


if __name__ == "__main__":
    load_data()
