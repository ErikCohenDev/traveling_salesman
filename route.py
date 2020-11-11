from datetime import datetime, timedelta
from location import Location
import config as cfg
from distance import (
    get_distance,
    get_closest_next_location,
    get_miles_of_route,
)
from delivery import Delivery
from typing import List


class Route:
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
        # Big O(n)
        if self._miles_driven == 0:
            return self._route[0]
        if self.route_complete is True:
            return self._route[-1]

        miles_driven_accumulator = 0
        for loc_idx, location in enumerate(self._route):
            delivered_location = self._route[loc_idx + 1]
            driven_distance = get_distance(location.address, delivered_location.address)
            if miles_driven_accumulator + driven_distance > self._miles_driven:
                return delivered_location
            miles_driven_accumulator += driven_distance

    def get_miles(self):
        # Big O(n)
        return get_miles_of_route(self.starting_location, self.deliveries)

    def add_delivery(self, truck_id, delivery, add_index):
        # Big O(n)
        delivery.set_assigned_truck(truck_id)
        if add_index is None:
            self.deliveries.append(delivery)
            return
        self.deliveries.insert(add_index, delivery)

    def add_deliveries(self, truck_id, deliveries_list: List[Delivery]):
        # Big O(n)
        for delivery in deliveries_list:
            delivery.set_assigned_truck(truck_id)
        self.deliveries += deliveries_list

    def get_next_delivery(self):
        # Big O(n)
        try:
            return next(delivery for delivery in self.deliveries if delivery.delivered is False)
        except StopIteration:
            return None

    def get_miles_left(self):
        # Big O(n)
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

    def added_distance_from_delivery_list(self, delivery_list):
        # Big O(n)
        added_distance = 0
        for delivery in delivery_list:
            added_distance = self.added_distance(delivery)
        return added_distance

    def added_distance(self, delivery_to_measure: Delivery):
        # Big O(n)
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
        # Big O(n)
        self._departure_time = time
        for delivery in self.deliveries:
            if self._route[-1].address != delivery.location:
                self._route.append(delivery.location)

    def is_route_complete(self):
        # Big O(n)
        return self.route_complete or self.get_next_location() is None

    def get_miles_to_next_location(self):
        next_location = self.get_next_location()
        if next_location is None:
            return None
        return get_distance(self._current_location.address, next_location.address)

    def miles_to_minutes(self, miles):
        # Big O(1)
        return miles / 0.3  # 18MPH / 60 mins

    def miles_traveled_time_delivered(self, miles):
        # Big O(1)
        minutes_to_add = self.miles_to_minutes(miles)
        dt_delivered = datetime.combine(datetime.today(), self._departure_time) + timedelta(minutes=minutes_to_add)
        return dt_delivered.time()

    def return_to_base(self, truck_id):
        # Big O(n)
        drive_distance = get_distance(self._current_location.address, self.starting_location.address)
        self._miles_driven += drive_distance
        timestamp = self.miles_traveled_time_delivered(self._miles_driven)
        self._current_location = self.starting_location
        self.time_route_complete = timestamp
        print(f'Truck {truck_id} back at base at', timestamp)

    def advance_by_miles(self, new_miles_driven):
        # Big O(n)
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


def calculate_route(deliveries):
    # Big O(n)
    route = [cfg.starting_location]
    pending_deliveries = list(deliveries.keys())
    miles = 0
    while len(pending_deliveries) > 0:
        last_travel_point_address = route[
            len(route) - 1
        ].address  # last location in our route
        closest_next_location = get_closest_next_location(
            last_travel_point_address, pending_deliveries
        )
        next_location, next_location_distance = closest_next_location
        miles = miles + next_location_distance
        pending_deliveries.remove(next_location)
        route.append([x for x in cfg.locations if x.address == next_location][0])
    print(get_distance(route[len(route) - 1].address, cfg.locations[0].address))
    return route
