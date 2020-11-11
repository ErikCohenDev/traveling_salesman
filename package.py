import config as cfg


class Package:
    def __init__(self, id_, location, deadline, weight, notes):
        self.id = id_
        self.location = location
        self.deadline = deadline
        self.assigned_truck = None
        self.weight = weight
        self.notes = notes

    def update_location(self, location):
        # Big O(1)
        self.location = location
        return self


def get_package_by_id(_id):
    # Big O(n)
    return [package for package in cfg.packages if package.id == _id][0]


def get_packages_with_unassigned_trucks():
    # Big O(n)
    return [package for package in cfg.packages if package.assigned_truck is None]
