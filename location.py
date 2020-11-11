import config as cfg


class Location:
    def __init__(self, id_, name, address):
        self.id = id_
        self.name = name
        self.address = address

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state

    def set_zip_code(self, zip_code):
        self.zip_code = zip_code


def get_location_by_address(address):
    # Big O(n)
    return [location for location in cfg.locations if location.address == address][0]
