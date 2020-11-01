from debug import print_delivery_count_by_truck, print_miles_report, print_package_count_by_truck
from typing import List
from csv_import import load_data
from delivery import Delivery, create_deliveries, get_deliveries_from_package_id_list, get_deliveries_with_unassigned_trucks
import config as cfg
from distance import get_distance
from truck import Truck


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
    init_data()

    truck1: Truck = cfg.trucks[0]
    truck2: Truck = cfg.trucks[1]
    truck3: Truck = cfg.trucks[2]

    deliveries_for_truck_two = get_deliveries_from_package_id_list(
        cfg.packages_that_must_be_on_truck_2
    )
    truck2.assign_deliveries(deliveries_for_truck_two)

    unassigned_deliveries = get_deliveries_with_unassigned_trucks()

    restrictions_packages = [
        *cfg.packages_that_must_go_together,
        *cfg.packages_that_leave_at_9_05,
        *cfg.packages_that_leave_at_10_20
    ]

    unassigned_deliveries_without_restrictions = []
    for delivery in unassigned_deliveries:
        for package in delivery.packages:
            if package.id not in restrictions_packages and delivery not in unassigned_deliveries_without_restrictions:
                unassigned_deliveries_without_restrictions.append(delivery)

    for delivery in unassigned_deliveries_without_restrictions:
        closest_truck = None
        closest_truck_distance = None
        route_add_index = None
        for truck in cfg.trucks:
            if truck.will_fit(delivery):
                (added_distance, add_index) = truck.route.added_distance(delivery)
                if closest_truck is None or added_distance < closest_truck_distance:
                    closest_truck = truck
                    closest_truck_distance = added_distance
                    route_add_index = add_index
        closest_truck.assign_delivery(delivery, route_add_index)

    deliveries_that_go_together: List[Delivery] = get_deliveries_from_package_id_list(
        cfg.packages_that_must_go_together
    )

    print_package_count_by_truck()


if __name__ == "__main__":
    main()
