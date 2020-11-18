from package import get_packages_with_unassigned_trucks
from delivery import get_deliveries_with_unassigned_trucks
import config as cfg


def print_miles_report():
    """
    Complexity: Big O(n)
    Print a report which lists the amount of miles driven by each truck
    """
    truck1_miles, truck2_miles, truck3_miles = [truck.route.get_miles() for truck in cfg.trucks]

    print(f"Truck1 Miles: {truck1_miles}")
    print(f"Truck2 Miles: {truck2_miles}")
    print(f"Truck3 Miles: {truck3_miles}")
    print(truck1_miles + truck2_miles + truck3_miles)


def print_delivery_count_by_truck():
    """
    Complexity: Big O(n)
    Print a report which lists the deliveries delivered by truck.
    The total assigned and unassigned deliveries
    """
    truck1_deliveries, truck2_deliveries, truck3_deliveries = [len(truck.get_deliveries()) for truck in cfg.trucks]

    print(f"Truck1 Deliveries: {truck1_deliveries}")
    print(f"Truck2 Deliveries: {truck2_deliveries}")
    print(f"Truck3 Deliveries: {truck3_deliveries}")
    print(f"Total Deliveries Assigned: {truck1_deliveries + truck2_deliveries + truck3_deliveries}")
    print(f"unassigned deliveries: {len(get_deliveries_with_unassigned_trucks())}")


def print_package_count_by_truck():
    """
    Complexity: Big O(n)
    Print a report which lists the amount packages assigned to each truck
    The total assigned and unassigned packages
    """
    truck1_packages, truck2_packages, truck3_packages = [len(truck.get_packages()) for truck in cfg.trucks]

    print(f"Truck1 packages: {truck1_packages}")
    print(f"Truck2 packages: {truck2_packages}")
    print(f"Truck3 packages: {truck3_packages}")
    print(f"Total packages Assigned: {truck1_packages + truck2_packages + truck3_packages}")
    print(f"unassigned packages: {len(get_packages_with_unassigned_trucks())}")


def print_package_table():
    """
    Complexity: Big O(n)
    Print a Table which lists the id, address, truck assigned, deadline and any notes of each package
    """
    print("___________________________________________________________________")
    print("____________________________PACKAGES_______________________________")
    print("id | Address                                | Truck      | Deadline | Notes ")
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
            f"{package_id} | {package_address} | {package_truck} | {package_deadline} | {package_notes}"
        )


def print_delivery_table(deliveries_list):
    """
    Complexity: Big O(n^2)
    Print a Table which lists the id, address, truck assigned, packages, and deadline of each delivery
    """
    print("_______________________________________________________________________________________")
    print("____________________________DELIVERIES_________________________________________________")
    print("id | Address                                | Truck      | packages | deadline | ETA ")
    for delivery in deliveries_list:
        # Pad the strings to take the same amount of space
        delivery_id = "{:<2}".format(delivery.id)
        delivery_address = "{:<38}".format(delivery.location.address)
        delivery_truck = (
            "{:<10}".format(delivery.assigned_truck)
            if delivery.assigned_truck is not None
            else "unassigned"
        )
        packages = "{:<8}".format(','.join([str(package.id) for package in delivery.packages]))
        delivery_deadline = delivery.earliest_deadline()
        delivery_ETA = delivery.ETA
        print(
            f"{delivery_id} | {delivery_address} | {delivery_truck} | {packages} | {delivery_deadline} | {delivery_ETA}"
        )
    print("_____________________________________________________________________")


def print_truck_table():
    """
    Complexity: Big O(n^2)
    Print a Table which lists the id, current location, deliveries, packages of each truck
    """
    print("_____________________________________________________________________")
    print("______________________________Trucks_________________________________")
    print("id | Current Location                       | Deliveries | Packages |")
    for truck in cfg.trucks:
        # Pad the strings to take the same amount of space
        truck_id = "{:<2}".format(truck.id)
        truck_location = "{:<38}".format(truck.route._current_location.address)
        deliveries_assigned = "{:<10}".format(len(truck.route.deliveries))
        packages_assigned = "{:<8}".format(sum(len(delivery.packages) for delivery in truck.route.deliveries))
        print(
            f"{truck_id} | {truck_location} | {deliveries_assigned} | {packages_assigned} |"
        )
    print("_____________________________________________________________________")


def print_route_table():
    """
    Complexity: Big O(n^2)
    Print list of addresses in the route assigned to each truck
    """
    print("_____________________________________________________________________")
    print("______________________________Routes_________________________________")
    for truck in cfg.trucks:
        print(f'Route assigned to truck {truck.id}')
        for delivery in truck.route.deliveries:
            print(f' |- {delivery.location.address}')


def print_current_time():
    """
    Complexity: Big O(n^2)
    print the global simulated time of the app
    """
    print(
        '________________________________\nThe current time is:',
        cfg.app_time,
        '\n________________________________\n'
    )
