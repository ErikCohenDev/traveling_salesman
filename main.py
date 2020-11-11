from datetime import datetime
from package import get_package_by_id
from location import get_location_by_address
from csv_import import load_data
from delivery import create_deliveries, get_deliveries_from_package_id_list, get_deliveries_without_restrictions, get_delivery_from_address, get_delivery_from_package_id
import config as cfg
from truck import Truck, assign_all_deliveries_to_best_truck, distribute_deliveries_to_trucks


def init_data():
    # Big O(n^2)
    """
    Load up all the data and store it in the config module
    """
    init_locations, init_distances, init_packages = load_data()
    cfg.init(init_locations, init_distances, init_packages)
    cfg.trucks = [Truck(1), Truck(2), Truck(3)]
    deliveries = create_deliveries()
    cfg.deliveries = deliveries


def main():
    # Big O(n^2)
    running = True
    init_data()

    truck1: Truck = cfg.trucks[0]
    truck2: Truck = cfg.trucks[1]
    truck3: Truck = cfg.trucks[2]

    non_restricted_deliveries = get_deliveries_without_restrictions()

    distribute_deliveries_to_trucks(non_restricted_deliveries)

    # Assign deliveries with restrictions
    deliveries_that_must_go_on_truck_2 = get_deliveries_from_package_id_list(cfg.packages_that_must_be_on_truck_2)
    truck2.assign_deliveries(deliveries_that_must_go_on_truck_2)

    # Assign delivery where package has wrong address
    # since it needs to be delivered after 10:20
    delivery_with_wrong_address = get_deliveries_from_package_id_list(cfg.packages_that_leave_at_10_20)
    delivery_that_leaves_at_9_05 = get_deliveries_from_package_id_list(cfg.packages_that_leave_at_9_05)
    truck3.assign_deliveries(delivery_that_leaves_at_9_05)
    truck3.assign_deliveries(delivery_with_wrong_address)

    deliveries_that_must_go_together = get_deliveries_from_package_id_list(cfg.packages_that_must_go_together)
    assign_all_deliveries_to_best_truck(deliveries_that_must_go_together)

    # start delivering
    truck1.start_delivering(cfg.app_time)

    today_10_20am = datetime.now().replace(hour=10, minute=20, second=0, microsecond=0).time()

    print('sum of Miles for all routes is', round(sum([truck.route.get_miles() for truck in cfg.trucks])), 'miles')
    while (running):
        if cfg.app_time >= today_10_20am and not delivery_with_wrong_address_is_fixed():
            fix_wrong_package_address_from_package_id(9, '410 S State St')
            truck2.start_delivering(cfg.app_time)
        option = input("press the Enter key to ff an hour, enter q to quit \n")
        if option == '':
            cfg.add_an_hour_to_global_time()
            for truck in cfg.trucks:
                if truck.started_delivering:
                    truck.an_hour_passed()
                if truck.id != 3 and truck.at_base() and truck.route.route_complete and truck3.started_delivering is False:
                    truck3.start_delivering(truck.route.time_route_complete)
            print('Current Time: ', cfg.app_time)
        else:
            running = False


def delivery_with_wrong_address_is_fixed():
    # Big O(n)
    delivery = get_delivery_from_package_id(9)
    return delivery.location.address == '410 S State St'


def fix_wrong_package_address_from_package_id(package_id, new_address):
    # Big O(n)
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
