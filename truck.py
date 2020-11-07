from route import Route
import config as cfg


class Truck:
    def __init__(self, _id):
        self.id = _id
        self.route = Route()
        self.miles_traveled = 0
        self.max_speed = 18  # Truck can reach a max speed of 18 MPH.
        self.completed_route = False
        self.departure_time = None
        self.started_delivering = False

    def assign_deliveries(self, deliveries_list):
        self.route.add_deliveries(self.id, deliveries_list)

    def at_base(self):
        return self.route._current_location == self.route.starting_location

    def assign_delivery(self, delivery, add_index):
        self.route.add_delivery(self.id, delivery, add_index)

    def assign_delivery_list(self, delivery_list):
        self.route.add_deliveries(self.id, delivery_list)

    def will_fit(self, delivery):
        return len(self.get_packages()) + len(delivery.packages) <= 16

    def will_fit_list(self, delivery_list):
        package_list_sum = sum([len(delivery.packages) for delivery in delivery_list])
        return len(self.get_packages()) + package_list_sum <= 16

    def get_deliveries(self):
        return [delivery for delivery in self.route.deliveries]

    def get_packages(self):
        return [delivery.packages for delivery in self.route.deliveries]

    def start_delivering(self, time):
        self.started_delivering = True
        self.route.init(time)
        self.departure_time = time
        print(f"Truck {self.id} has started its route at {time}")

    def an_hour_passed(self):
        miles_left = self.route.get_miles_left

        if self.completed_route or miles_left() == 0:
            if self.route._current_location != self.route.starting_location:
                self.route.return_to_base(self.id, 18)
            self.completed_route = True
            print(f"Truck {self.id} has completed route")
            return

        print(f"Truck {self.id} has {miles_left()} miles left to go")

        self.miles_traveled += self.max_speed

        self.route.advance_by_miles(18)

        print(f"Truck {self.id} has driven {self.miles_traveled} miles")

        if miles_left() == 0:
            self.completed_route = True
            print(f"Truck {self.id} has completed route")
            return


def distribute_deliveries_to_trucks(delivery_list):
    for delivery in delivery_list:
        closest_truck = None
        closest_truck_distance = None
        route_add_index = None
        for truck in cfg.trucks:
            if truck.will_fit(delivery):
                (added_distance, add_index) = truck.route.added_distance(delivery)
                if closest_truck is None or added_distance < closest_truck_distance:
                    closest_truck = truck
                    closest_truck_distance = added_distance
                    route_add_index = add_index
        closest_truck.assign_delivery(delivery, route_add_index)


def assign_all_deliveries_to_best_truck(delivery_list):
    closest_truck = None
    closest_truck_distance = None
    route_add_index = None
    for truck in cfg.trucks:
        if truck.will_fit_list(delivery_list):
            (added_distance, add_index) = truck.route.added_distance_from_delivery_list(delivery_list)
            if closest_truck is None or added_distance < closest_truck_distance:
                closest_truck = truck
                closest_truck_distance = added_distance
                route_add_index = add_index
    closest_truck.assign_delivery_list(delivery_list)
