from cli import CLI
from package import get_package_by_id
from location import get_location_by_address
from csv_import import load_data
from delivery import create_deliveries, get_delivery_from_address, get_delivery_from_package_id
import config as cfg
from truck import distribute_deliveries_to_trucks


def init_data():
    """'
    Big O(n^2)
    Load up all the data from the data folder instantiate the Objects for each
    and store it in the config module to be available globally
    """
    # Get the Data
    init_locations, init_distances, init_packages = load_data()

    # Save to global variables to make easily accessible
    cfg.init(init_locations, init_distances, init_packages)

    # Create deliveries of packages to specific locations
    deliveries = create_deliveries()
    cfg.deliveries = deliveries


def assign_deliveries():
    """'
    Create Routes from pending devlieries and
    Assign deliveries to all the available trucks
    """
    # get and distrubute deliveries without restrictions to available trucks
    distribute_deliveries_to_trucks()
    cfg.truck1.start_delivering(cfg.app_time)
    cfg.truck2.start_delivering(cfg.app_time)

    cfg.truck1.populate_ETA(cfg.app_time)
    cfg.truck2.populate_ETA(cfg.app_time)


def main():
    """'
    Big O(n^3)
    Initiate the application
    """
    init_data()
    assign_deliveries()
    CLI().run()


def delivery_with_wrong_address_is_fixed():
    """
    Complexity: Big O(n^2)
    Check if the Delivery with the wrong address has been fixed
    Returns: bool - has it been fixed?
    """
    delivery = get_delivery_from_package_id(9)
    return delivery.location.address == '410 S State St'


def fix_wrong_package_address(package_id, new_address):
    """
    Complexity: Big O(n^2)
    Fix the wrong package address
    update the deliveries the package is associated with
    """
    print(f'correcting wrong address for package {package_id}')
    correct_location = get_location_by_address(new_address)
    delivery_with_wrong_location = get_delivery_from_package_id(package_id)
    package_with_wrong_location = get_package_by_id(package_id)
    delivery_with_wrong_location.remove_package(package_with_wrong_location)
    delivery_with_correct_location = get_delivery_from_address(new_address)
    package_with_correct_address = package_with_wrong_location.update_location(correct_location)
    delivery_with_correct_location.add_package(package_with_correct_address)


if __name__ == "__main__":
    main()
