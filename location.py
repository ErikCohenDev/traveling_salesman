import config as cfg


class Location:
    def __init__(self, id_, name, address):
        self.id = id_
        self.name = name
        self.address = address


def get_location_by_address(address):
    return [location for location in cfg.locations if location.address == address][0]
