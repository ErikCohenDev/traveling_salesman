from datetime import datetime, timedelta
from location import Location
import config as cfg
from distance import (
    get_distance,
    get_closest_next_location,
    get_miles_of_route,
)
from math import ceil, floor
from delivery import Delivery
from typing import List


class Route:
    starting_location: Location
    _miles_driven = 0
    _miles_driven_up_to_previous_location = 0
    _current_location = None
    _departure_time = None

    def __init__(self):
        self.deliveries: List[Delivery] = []
        self.starting_location = cfg.starting_location
        self._current_location = self.starting_location
        self._route: List[Location] = []
        self._route.append(self.starting_location)
        self.minutes_driving = 0
        self.last_delivery_timestamp = cfg.app_time

    def get_next_location(self):
        current_location_idx = self._route.index(self._current_location)
        try:
            next_location = self._route[current_location_idx + 1]
        except IndexError:
            return None
        return next_location

    def get_miles(self):
        return get_miles_of_route(self.starting_location, self.deliveries)

    def add_delivery(self, truck_id, delivery, add_index):
        delivery.set_assigned_truck(truck_id)
        if add_index is None:
            self.deliveries.append(delivery)
            return
        self.deliveries.insert(add_index, delivery)

    def add_deliveries(self, truck_id, deliveries_list: List[Delivery]):
        for delivery in deliveries_list:
            delivery.set_assigned_truck(truck_id)
        self.deliveries += deliveries_list

    def get_next_delivery(self):
        next_location = self.get_next_location()
        if next_location is None:
            return None
        next_delivery = next(x for x in self.deliveries if x.location == next_location)
        return next_delivery

    def get_miles_left(self):
        current_location_idx = self._route.index(self._current_location)
        miles_left = 0
        for loc_idx, location in enumerate(self._route[current_location_idx:]):
            try:
                miles_left += get_distance(location.address, self._route[loc_idx + 1].address)
            except IndexError:
                if miles_left == 0:
                    return None
                return miles_left

    def added_distance(self, delivery_to_measure: Delivery):
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
        self._departure_time = time
        for delivery in self.deliveries:
            if self._route[-1].address != delivery.location:
                self._route.append(delivery.location)

    def is_route_complete(self):
        return self.get_next_location() is None

    def get_miles_to_next_location(self):
        next_location = self.get_next_location()
        if next_location is None:
            return None
        return get_distance(self._current_location.address, next_location.address)

    def miles_to_minutes(self, miles):
        return miles / 0.3  # 18MPH / 60 mins

    def advance_to_next_location(self):
        miles_to_next_location = self.get_miles_to_next_location()
        self._miles_driven_up_to_previous_location = self._miles_driven_up_to_previous_location + miles_to_next_location
        next_delivery = self.get_next_delivery()

        minutes_to_add = self.miles_to_minutes(miles_to_next_location)
        self.last_delivery_timestamp = (
            datetime.combine(datetime.today(), self.last_delivery_timestamp) + timedelta(minutes=minutes_to_add)
        ).time()

        print(f"delivered packages to {next_delivery.location.address} at {self.last_delivery_timestamp}")

        next_delivery.mark_as_delivered(self.last_delivery_timestamp)
        self._current_location = self.get_next_location()

    def new_miles_driven(self, hourly_miles_driven):
        miles_to_next_location = self.get_miles_to_next_location()

        # Push current location forward 18 miles

        end_of_hour_miles = self._miles_driven + hourly_miles_driven
        distance_to_next_location = self.get_miles_to_next_location()
        delivery_distance_miles = self._miles_driven + distance_to_next_location

        while delivery_distance_miles <= end_of_hour_miles:
            miles_to_next_location = self.get_miles_to_next_location()
            # Route has completed
            if miles_to_next_location is None:
                break
            self.advance_to_next_location()


def calculate_route(deliveries):
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
