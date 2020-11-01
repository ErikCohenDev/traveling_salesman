from package import get_packages_with_unassigned_trucks
from delivery import get_deliveries_with_unassigned_trucks
import config as cfg


def print_miles_report():
    truck1_miles, truck2_miles, truck3_miles = [truck.route.get_miles() for truck in cfg.trucks]

    print(f"Truck1 Miles: {truck1_miles}")
    print(f"Truck2 Miles: {truck2_miles}")
    print(f"Truck3 Miles: {truck3_miles}")
    print(truck1_miles + truck2_miles + truck3_miles)


def print_delivery_count_by_truck():
    truck1_deliveries, truck2_deliveries, truck3_deliveries = [len(truck.get_deliveries()) for truck in cfg.trucks]

    print(f"Truck1 Deliveries: {truck1_deliveries}")
    print(f"Truck2 Deliveries: {truck2_deliveries}")
    print(f"Truck3 Deliveries: {truck3_deliveries}")
    print(f"Total Deliveries Assigned: {truck1_deliveries + truck2_deliveries + truck3_deliveries}")
    print(f"unassigned deliveries: {len(get_deliveries_with_unassigned_trucks())}")


def print_package_count_by_truck():
    truck1_packages, truck2_packages, truck3_packages = [len(truck.get_packages()) for truck in cfg.trucks]

    print(f"Truck1 packages: {truck1_packages}")
    print(f"Truck2 packages: {truck2_packages}")
    print(f"Truck3 packages: {truck3_packages}")
    print(f"Total packages Assigned: {truck1_packages + truck2_packages + truck3_packages}")
    print(f"unassigned packages: {len(get_packages_with_unassigned_trucks())}")


def print_package_table():
    print("id | Address                                | Truck      |  Deadline                | Notes ")
    for package in cfg.packages:
        # Pad the strings to take the same amount of space
        package_id = "{:<2}".format(package.id)
        package_address = "{:<38}".format(package.location.address)
        package_truck = (
            "{:<10}".format(package.assigned_truck)
            if package.assigned_truck is not None
            else "unassigned"
        )
        package_deadline = package.deadline.strftime("%H:%M %p")
        package_notes = package.notes if package.notes is not False else "N/A"
        print(
            f"{package_id} | {package_address} | {package_truck} | \
                {package_deadline} | {package_notes}"
        )


def print_delivery_table():
    # TODO Implement
    pass


def print_truck_table():
    # TODO Implement
    pass


def print_route_table():
    # TODO Implement
    pass
