import config as cfg


class Package:
    """
    The Package Class is a representation of an item delivered to an location
    """
    def __init__(self, id_, location, deadline, weight, notes):
        self.id = id_
        self.location = location
        self.deadline = deadline
        self.assigned_truck = None
        self.weight = weight
        self.notes = notes

    def update_location(self, location):
        """
        Complexity: Big O(1)
        update the location of a package
        """
        self.location = location
        return self


def get_package_by_id(_id):
    """
    Complexity: Big O(n)
    get a package by its ID number
    """
    return [package for package in cfg.packages if package.id == _id][0]


def get_packages_with_unassigned_trucks():
    """
    Complexity: Big O(n)
    get packages that do not have a truck assigned
    """
    return [package for package in cfg.packages if package.assigned_truck is None]
