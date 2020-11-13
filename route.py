from datetime import datetime, timedelta
from location import Location
import config as cfg
from distance import (
    get_distance,
    get_miles_of_route,
)
from delivery import Delivery
from typing import List


class Route:
    """
    The Route Object is a sorted list of Locations
    which is optimized for the Truck to follow to disburse Deliveries
    """
    starting_location: Location
    _miles_driven = 0
    _departure_time = None

    def __init__(self):
        self.deliveries: List[Delivery] = []
        self.starting_location = cfg.starting_location
        self._route: List[Location] = []
        self._route.append(self.starting_location)
        self._current_location = self.starting_location
        self.minutes_driving = 0
        self.route_complete = False
        self.time_route_complete = None

    def get_current_location(self):
        """
        Complexity: Big O(n)
        Get the current location of truck within the route
        """
        if self._miles_driven == 0:
            return self._route[0]
        if self.route_complete is True:
            return self._route[-1]

        miles_driven_accu = 0
        for loc_idx, location in enumerate(self._route):
            delivered_location = self._route[loc_idx + 1]
            driven_distance = get_distance(location.address, delivered_location.address)
            if miles_driven_accu + driven_distance > self._miles_driven:
                return delivered_location
            miles_driven_accu += driven_distance

    def get_miles(self):
        """
        Complexity: Big O(n)
        Get distance of miles of traveling the complete route
        """
        return get_miles_of_route(self.starting_location, self.deliveries)

    def add_delivery(self, truck_id, delivery, add_index):
        """
        Complexity: Big O(n)
        Add a delivery to this route
        """
        delivery.set_assigned_truck(truck_id)
        if add_index is None:
            self.deliveries.append(delivery)
            return
        self.deliveries.insert(add_index, delivery)

    def add_deliveries(self, truck_id, deliveries_list: List[Delivery]):
        """
        Complexity: Big O(n)
        Add a List of deliveries to this route
        """
        for delivery in deliveries_list:
            delivery.set_assigned_truck(truck_id)
        self.deliveries += deliveries_list

    def get_next_delivery(self):
        """
        Complexity: Big O(n)
        If there is a next delivery return it else return None
        """
        try:
            return next(delivery for delivery in self.deliveries if delivery.delivered is False)
        except StopIteration:
            return None

    def get_miles_left(self):
        """
        Complexity: Big O(n)
        Get the amount of miles left for this route
        """
        if not self.get_next_delivery():
            return 0
        current_location = self._current_location
        current_location_idx = self._route.index(current_location)
        miles_left = 0
        for loc_idx, location in enumerate(self._route[current_location_idx:]):
            try:
                miles_left += get_distance(location.address, self._route[loc_idx + 1].address)
            except IndexError:
                return round(miles_left, 2)
        return round(miles_left, 2)

    def get_miles_to_index(self, index):
        """
        Complexity:
        get the amount of miles until a certain index in the route
        """
        miles = 0

    def added_distance_from_delivery_list(self, delivery_list):
        """
        Complexity: Big O(n)
        Calculates How many miles would be added if appending the delivery list to this route
        """
        added_distance = 0
        for delivery in delivery_list:
            added_distance = self.added_distance(delivery)
        return added_distance

    def added_distance(self, delivery_to_measure: Delivery):
        """
        Complexity: Big O(n)
        Calculate HOw many miles would be added if appending this delivery to this route
        """
        if len(self.deliveries) == 0:
            return get_distance(self.starting_location.address, delivery_to_measure.location.address), None

        min_distance = None
        add_index = None
        for index in range(0, len(self.deliveries) + 1):
            deliveries_copy = self.deliveries.copy()
            deliveries_copy.insert(index, delivery_to_measure)
            added_distance_for_delivery = get_miles_of_route(self.starting_location, deliveries_copy)
            if (min_distance is None or added_distance_for_delivery < min_distance):
                min_distance = round(added_distance_for_delivery, 2)
                add_index = index
        return (min_distance, add_index)

    def init(self, time):
        """
        Complexity: Big O(n)
        Initialize the route to start delivering
        """
        self._departure_time = time
        for delivery in self.deliveries:
            if self._route[-1].address != delivery.location:
                self._route.append(delivery.location)

    def is_route_complete(self):
        """
        Complexity: Big O(n)
        Has this route completed its route
        """
        return self.route_complete or self.get_next_location() is None

    def get_miles_to_next_location(self):
        """
        Complexity: Big O(n)
        return the amount of miles to the next delivery location
        """
        next_location = self.get_next_location()
        if next_location is None:
            return None
        return get_distance(self._current_location.address, next_location.address)

    def miles_to_minutes(self, miles):
        """
        Complexity: Big O(1)
        Transform the amount of miles into minutes traveled
        """
        return miles / 0.3  # 18MPH / 60 mins

    def miles_traveled_time_delivered(self, miles):
        """
        Complexity: Big O(1)
        Calculate when a delivery was delivered by how many miles were traveled
        """
        minutes_to_add = self.miles_to_minutes(miles)
        dt_delivered = datetime.combine(datetime.today(), self._departure_time) + timedelta(minutes=minutes_to_add)
        return dt_delivered.time()

    def return_to_base(self, truck_id):
        """
        Complexity: Big O(n)
        When the route is complete instuct return the Truck back to base
        """
        drive_distance = get_distance(self._current_location.address, self.starting_location.address)
        self._miles_driven += drive_distance
        timestamp = self.miles_traveled_time_delivered(self._miles_driven)
        self._current_location = self.starting_location
        self.time_route_complete = timestamp
        print(f'Truck {truck_id} back at base at', timestamp)

    def advance_by_miles(self, new_miles_driven):
        """
        Complexity: Big O(n)
        Move the route forward the amount of the new miles driven.
        """
        miles_driven_acc = self._miles_driven
        self._miles_driven += new_miles_driven

        while self.get_next_delivery():
            next_delivery = self.get_next_delivery()
            drive_distance = get_distance(self._current_location.address, next_delivery.location.address)
            if miles_driven_acc + drive_distance > self._miles_driven:
                break
            miles_driven_acc += drive_distance
            timestamp = self.miles_traveled_time_delivered(miles_driven_acc)
            next_delivery.mark_as_delivered(timestamp)
            self._current_location = next_delivery.location

        if self.get_next_delivery() is None:
            self._current_location = self.deliveries[-1].location
            self.route_complete = True
