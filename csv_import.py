"""
Erik Cohen
Student #000915169
"""
import csv

from package import Package
from hash_table import HashTable
from location import Location
from datetime import datetime


def get_locations():
    """
    Complexity: Big O(N)
    Get all the location data from the CSV and create a location object
    """
    locations = []
    with open("./data/locations.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            locations.append(Location(int(row["id"]), row["name"], row["address"]))
        return locations


def get_distances(locations):
    """
    Complexity: Big O(N^2)
    Get all the distances from the csv file and create a distances hashtable
    We will use the hash table later to compute the distance from one location to another
    """
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
    """
    Complexity: Big O(1)
    parse the deadline string into a deadline datetime
    if deadline is not present set the deadline to 17:00 as the End of the working day
    object to be able to better calculate times to deadline
    """
    EOD_time = datetime.strptime("17:00:00", "%H:%M:%S").time()
    now = datetime.today()
    if deadline == "EOD":
        return datetime.combine(now, EOD_time)
    deadline_time = datetime.strptime(deadline, "%H:%M:%S").time()
    dt = datetime.combine(now, deadline_time)
    return dt


def parse_notes(note):
    """
    Complexity: Big O(1)
    Tread N/A as a falsy value
    """
    if note == "N/A":
        return False
    return note


def get_packages(locations):
    """
    Complexity: Big O(N)
    get all the package data from the csv and create Package class instances
    append additional data to the location object which it did not previously have
    match the location address of the package with a location instance already created to make mapping simpler.
    """
    packages = []
    with open("./data/packages.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            package_location = [
                location for location in locations if location.address == row["address"]
            ][0]

            package_location.set_city(row["city"])
            package_location.set_state(row["state"])
            package_location.set_zip_code(row["zip"])

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
    """
    Complexity: Big O(N^2)
    Initiate all the get_* functions to initialize all the data needed to start our application
    """
    locations = get_locations()
    return locations, get_distances(locations), get_packages(locations)


if __name__ == "__main__":
    # Big O(N^2)
    load_data()
