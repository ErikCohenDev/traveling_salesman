from route import Route


class Truck:
    def __init__(self, _id):
        self.id = _id
        self.route = Route()
        self.miles_traveled = 0
        self.max_speed = 18  # Truck can reach a max speed of 18 MPH.

    def assign_deliveries(self, deliveries_list):
        self.route.add_deliveries(self.id, deliveries_list)

    def assign_delivery(self, delivery, add_index):
        self.route.add_delivery(self.id, delivery, add_index)

    def will_fit(self, delivery):
        return len(self.get_packages()) + len(delivery.packages) <= 16

    def get_deliveries(self):
        return [delivery for delivery in self.route.deliveries]

    def get_packages(self):
        return [delivery.packages for delivery in self.route.deliveries]
