from cli import CLI
from csv_import import load_data
from delivery import Delivery, create_deliveries, get_deliveries_from_package_id_list
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

    deliveries_that_go_together = get_deliveries_from_package_id_list(
        cfg.packages_that_must_go_together
    )


if __name__ == "__main__":
    main()
