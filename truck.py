from datetime import datetime
from delivery import get_deliveries_from_package_id_list, get_deliveries_with_unassigned_trucks
from route import Route
import config as cfg


class Truck:
    def __init__(self, _id):
        self.id = _id
        self.route = Route()
        self.miles_traveled = 0
        self.max_speed = 18  # Truck can reach a max speed of 18 MPH.
        self.max_packages = 16  # Truck can contain a max of 16 packages per route
        self.completed_route = False
        self.departure_time = None
        self.started_delivering = False

    def at_base(self):
        """
        Complexity: Big O(1)
        Returns if the truck is at starting location
        """
        return self.route._current_location == self.route.starting_location

    def assign_delivery(self, delivery, add_index):
        """
        Complexity: Big O(1)
        assign a single delivery at a specific index
        """
        self.route.add_delivery(self.id, delivery, add_index)

    def assign_deliveries(self, deliveries_list):
        """
        Complexity: Big O(n)
        Assign a List of deliveries to this Truck
        """
        self.route.add_deliveries(self.id, deliveries_list)

    def will_fit(self, delivery):
        """
        Complexity: Big O(n)
        Checks to see if this delivery will fit in the Truck
        """
        return len(self.get_packages()) + len(delivery.packages) <= self.max_packages

    def will_fit_list(self, delivery_list):
        """
        Complexity: Big O(n)
        Checks to see if this list of deliveries will fit in the Truck
        """
        package_list_sum = sum([len(delivery.packages) for delivery in delivery_list])
        return len(self.get_packages()) + package_list_sum <= 16

    def get_deliveries(self):
        """
        Complexity: Big O(n)
        Get all the deliveries assigned to this truck
        """
        return [delivery for delivery in self.route.deliveries]

    def get_packages(self):
        """
        Complexity: Big O(n)
        Get all the packages assigned to this truck
        """
        package_list = []
        for delivery in self.route.deliveries:
            package_list += delivery.packages
        return package_list

    def start_delivering(self, time):
        """
        Complexity: Big O(1)
        Start the route and timestamp the departure time of the truck
        """
        self.started_delivering = True
        self.route.init(time)
        self.departure_time = time
        print(f"Truck {self.id} has started its route at {time}")

    def minutes_passed(self, minutes):
        """
        Complexity: Big O(n)
        Notify this truck a specified amount of minutes have passed.
        Convert the time to miles and advance the route
        """
        miles_left = self.route.get_miles_left
        miles_traveled = 0.3 * minutes
        if self.completed_route or miles_left() == 0:
            if self.route._current_location != self.route.starting_location:
                self.route.return_to_base(self.id)
            self.completed_route = True
            print(f"Truck {self.id} has completed route")
            return
        print(f"Truck {self.id} has {miles_left()} miles left to go")
        self.miles_traveled += miles_traveled
        self.route.advance_by_miles(miles_traveled)
        print(f"Truck {self.id} has driven {round(self.miles_traveled, 2)} miles")
        if miles_left() == 0:
            self.completed_route = True
            print(f"Truck {self.id} has completed route")
            return

    def get_ETA_back_at_depot(self):
        return self.route.get_ETA_back_at_depot()

    def populate_ETA(self, departure_time):
        """
        Complexity: Big O(n^2)
        """
        self.route.populate_ETA(departure_time)


def distribute_deliveries_to_trucks():
    """
    Complexity: Big O(n^2)
    Calculate the added milage for each route assigned to each truck.
    Determine the truck which the delivery would increase the milage
    the least and its position within the route.
    Assign it to the best truck at the best position
    """
    assign_deliveries_truck_2()
    deliveries_with_unassigned_trucks = get_deliveries_with_unassigned_trucks()
    now = datetime.today()
    start_of_day_time = datetime.strptime("08:00:00", "%H:%M:%S").time()
    start_of_day = datetime.combine(now, start_of_day_time).time()
    for delivery in deliveries_with_unassigned_trucks:
        closest_truck = None
        closest_truck_distance = None
        route_add_index = None
        for truck in cfg.trucks:
            if truck.will_fit(delivery):
                delivery_departure = None
                if (truck.id == 1 or truck.id == 2):
                    delivery_departure = start_of_day
                elif (truck.id == 3):
                    estimated_time_back_at_depot = datetime.strptime("10:30:00", "%H:%M:%S").time()
                    delivery_departure = datetime.combine(now, estimated_time_back_at_depot).time()
                (added_distance, add_index) = truck.route.added_distance(delivery_departure, delivery)
                if (added_distance is None and add_index is None):
                    continue
                if closest_truck is None or added_distance < closest_truck_distance:
                    closest_truck = truck
                    closest_truck_distance = added_distance
                    route_add_index = add_index

        closest_truck.assign_delivery(delivery, route_add_index)

def assign_deliveries_truck_2():
    """
    Complexity: Big O(n)
    """
    deliveries_that_must_go_on_truck_2 = get_deliveries_from_package_id_list(cfg.packages_that_must_be_on_truck_2)
    cfg.truck2.assign_deliveries(deliveries_that_must_go_on_truck_2)
