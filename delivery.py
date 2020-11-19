import config as cfg


class Delivery:
    """
    A Delivery aggregates a list of packages which are assigned the same location
    """
    _class_counter = 0

    def __init__(self, location, packages=[]):
        Delivery._class_counter += 1
        self.location = location
        self.packages = packages
        self.assigned_truck = None
        self.delivered_time = None
        self.delivered = False
        self.id = Delivery._class_counter
        self.ETA = None

    def earliest_deadline(self):
        """
        Complexity: Big O(n)
        Return the time of the package which has to arrive the earliest to its destination
        """
        return min([package.deadline.time() for package in self.packages if package.deadline.time()])

    def set_ETA(self, ETA):
        self.ETA = ETA

    def add_package(self, package):
        """
        Complexity: Big O(1)
        Add the package to this delivery
        """
        self.packages.append(package)

    def remove_package(self, package):
        """
        Complexity: Big O(1)
        Remove the package from this delivery
        """
        self.packages.remove(package)

    def has_package_id(self, _id):
        """
        Complexity: Big O(n)
        Check if this package id exists within the packages list
        """
        return len([package for package in self.packages if package.id == _id]) > 0

    def set_assigned_truck(self, num):
        """
        Complexity: Big O(n)
        Set the id of the truck that this delivery and packages are assigned to
        """
        self.assigned_truck = num
        for package in self.packages:
            package.assigned_truck = num

    def mark_as_delivered(self, time_delivered):
        """
        Complexity: Big O(1)
        Mark the delivery as delivered and log the instance, time of delivery
        """
        print(f"Truck {self.assigned_truck} delivered packages to {self.location.address} at {time_delivered}")
        self.delivered_time = time_delivered
        self.delivered = True


def create_deliveries():
    """
    Complexity: Big O(n^2)
    Create a list of deliveries from all the packages defined globally in the app
    """
    wrong_package_id = 9
    deliveries = []
    for location in cfg.locations:
        packages_for_location = []
        for package in cfg.packages:
            if package.location == location and package.id is not wrong_package_id:
                packages_for_location.append(package)
        if len(packages_for_location) > 0:
            deliveries.append(Delivery(location, packages_for_location))
    return deliveries


def get_delivery_from_package_id(package_id):
    """
    Complexity: Big O(n^2)
    Get a Delivery that contains a package with a specific id
    """
    for delivery in cfg.deliveries:
        for package in delivery.packages:
            if package.id == package_id:
                return delivery


def get_deliveries_from_package_id_list(packages_id_list):
    """
    Complexity: Big O(n)
    Get a list of deliveries which contain an id from a list of packages
    """
    delivery_list = []
    for _id in packages_id_list:
        delivery_list.append(get_delivery_from_package_id(_id))
    return delivery_list


def get_deliveries_with_unassigned_trucks():
    """
    Complexity: Big O(n^2)
    Get all the deliveries which do not have a truck assigned
    """
    deliveries_with_unassigned_packages = []
    for delivery in cfg.deliveries:
        for package in delivery.packages:
            if (package.assigned_truck is None and delivery not in deliveries_with_unassigned_packages):
                deliveries_with_unassigned_packages.append(delivery)
    return deliveries_with_unassigned_packages


def get_number_of_packages_for_delivery_list(delivery_list):
    """
    Complexity: Big O(n^2)
    Get the number of packages from a list of deliveries
    """
    packages_count = 0
    for delivery in delivery_list:
        packages_count += len(delivery.packages)
    return packages_count


def filter_deliveries_with_package_id_list(package_id_list):
    """
    Complexity: Big O(n^2)
    Return a list of deliveries which do not contain an id from the package list
    """
    deliveries_without_filter = []
    for delivery in cfg.deliveries:
        check_if_contains_filter = any([package for package in delivery.packages if package.id in package_id_list])
        if check_if_contains_filter:
            deliveries_without_filter.append(delivery)
    return deliveries_without_filter


def get_deliveries_without_restrictions():
    """
    Complexity: Big O(n^2)
    Get a List of Deliveries which do not have a restriction
    """
    deliveries_without_filter = []
    for delivery in cfg.deliveries:
        check_if_has_restriction = any(
            [package for package in delivery.packages if package.id in cfg.packages_restrictions]
        )
        if not check_if_has_restriction:
            deliveries_without_filter.append(delivery)
    return deliveries_without_filter


def get_deliveries_with_restrictions():
    """
    Complexity: Big O(n^2)
    Get the deliveries that have some kind of restriction
    """
    deliveries_without_filter = []
    for delivery in cfg.deliveries:
        check_if_has_restriction = any(
            [package for package in delivery.packages if package.id in cfg.packages_restrictions]
        )
        if check_if_has_restriction:
            deliveries_without_filter.append(delivery)
    return deliveries_without_filter


def get_delivery_from_address(address):
    """
    Complexity: Big O(n)
    Static method to get the delivery by the Address String of a location
    """
    return [delivery for delivery in cfg.deliveries if delivery.location.address == address][0]
