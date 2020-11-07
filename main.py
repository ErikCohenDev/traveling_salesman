from debug import print_delivery_count_by_truck, print_delivery_table, print_miles_report, print_package_count_by_truck, print_package_table, print_route_table, print_truck_table
from typing import List
from csv_import import load_data
from delivery import Delivery, create_deliveries, filter_deliveries_with_package_id_list, get_deliveries_from_package_id_list, get_deliveries_with_restrictions, get_deliveries_with_unassigned_trucks, get_deliveries_without_restrictions
import config as cfg
from distance import get_distance
from truck import Truck, assign_all_deliveries_to_best_truck, distribute_deliveries_to_trucks


def init_data():
    """
    Load up all the data and store it in the config file
    """
    init_locations, init_distances, init_packages = load_data()
    cfg.init(init_locations, init_distances, init_packages)
    cfg.trucks = [Truck(1), Truck(2), Truck(3)]
    deliveries = create_deliveries()
    cfg.deliveries = deliveries


def main():
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
    truck2.start_delivering(cfg.app_time)

    while (running):
        option = input("press the 1 to ff an hour: \n")
        if option == '1':
            cfg.add_an_hour_to_global_time()
            for truck in cfg.trucks:
                if truck.started_delivering:
                    truck.an_hour_passed()
                if truck.id != 3 and truck.at_base() and truck3.started_delivering is False:
                    truck3.start_delivering(truck.route.time_route_complete)
            print('Current Time: ',cfg.app_time)
        else:
            running = False


if __name__ == "__main__":
    main()
