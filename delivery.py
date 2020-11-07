import config as cfg
from location import Location
from package import Package
from typing import List


class Delivery:
    _class_counter = 0

    def __init__(self, location, packages=[]):
        Delivery._class_counter += 1
        self.location: Location = location
        self.packages: List[Package] = packages
        self.assigned_truck = None
        self.delivered_time = None
        self.delivered: bool = False
        self.id = Delivery._class_counter

    def add_package(self, package):
        self.packages.append(package)

    def has_package_id(self, _id):
        return len([package for package in self.packages if package.id == _id]) > 0

    def set_assigned_truck(self, num):
        self.assigned_truck = num
        for package in self.packages:
            package.assigned_truck = num

    def mark_as_delivered(self, time_delivered):
        print(f"delivered packages to {self.location.address} at {time_delivered}")
        self.delivered_time = time_delivered
        self.delivered = True


def create_deliveries():
    deliveries: List[Delivery] = []
    for location in cfg.locations:
        packages_for_location = []
        for package in cfg.packages:
            if package.location == location:
                packages_for_location.append(package)
        if len(packages_for_location) > 0:
            deliveries.append(Delivery(location, packages_for_location))
    return deliveries


def get_delivery_from_package_id(package_id):
    for delivery in cfg.deliveries:
        for package in delivery.packages:
            if package.id == package_id:
                return delivery


def get_deliveries_from_package_id_list(packages_id_list):
    delivery_list = []
    for _id in packages_id_list:
        delivery_list.append(get_delivery_from_package_id(_id))
    return delivery_list


def get_deliveries_with_unassigned_trucks():
    deliveries_with_unassigned_packages = []
    for delivery in cfg.deliveries:
        for package in delivery.packages:
            if (package.assigned_truck is None and delivery not in deliveries_with_unassigned_packages):
                deliveries_with_unassigned_packages.append(delivery)
    return deliveries_with_unassigned_packages


def get_number_of_packages_for_delivery_list(delivery_list):
    packages_count = 0
    for delivery in delivery_list:
        packages_count += len(delivery.packages)
    return packages_count


def filter_deliveries_with_package_id_list(package_id_list):
    deliveries_without_filter = []
    for delivery in cfg.deliveries:
        check_if_contains_filter = any([package for package in delivery.packages if package.id in package_id_list])
        if check_if_contains_filter:
            deliveries_without_filter.append(delivery)
    return deliveries_without_filter


def get_deliveries_without_restrictions():
    deliveries_without_filter = []
    for delivery in cfg.deliveries:
        check_if_has_restriction = any(
            [package for package in delivery.packages if package.id in cfg.packages_restrictions]
        )
        if not check_if_has_restriction:
            deliveries_without_filter.append(delivery)
    return deliveries_without_filter


def get_deliveries_with_restrictions():
    deliveries_without_filter = []
    for delivery in cfg.deliveries:
        check_if_has_restriction = any(
            [package for package in delivery.packages if package.id in cfg.packages_restrictions]
        )
        if check_if_has_restriction:
            deliveries_without_filter.append(delivery)
    return deliveries_without_filter
