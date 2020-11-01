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

    def __init__(self):
        self.deliveries: List[Delivery] = []
        self.starting_location = cfg.starting_location

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
