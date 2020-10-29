from route import Route


class Truck:
    def __init__(self, _id):
        self.id = _id
        self.route = Route()
        self.miles_traveled = 0
        self.max_speed = 18  # Truck can reach a max speed of 18 MPH.

    def assign_deliveries(self, deliveries_list):
        self.route.add_deliveries(deliveries_list)

    def will_fit_truck(self, delivery):
        return len(self.get_packages()) + len(delivery.packages) <= 16

    def get_packages(self):
        return [delivery.packages for delivery in self.route.deliveries]
