import config as cfg
from distance import (
    get_distance,
    get_closest_next_location,
    get_miles_closest_delivery_in_route,
    get_miles_of_route,
)
from delivery import Delivery
from typing import List


class Route:
    def __init__(self):
        self.deliveries: List[Delivery] = []

    def get_miles(self):
        return get_miles_of_route(self.deliveries)

    def add_delivery(self, delivery):
        pass

    def add_deliveries(self, deliveries_list: List[Delivery]):
        for delivery in deliveries_list:
            delivery.set_assigned_truck(2)
        self.deliveries += deliveries_list


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


def get_closest_route(delivery, route_truck_one, route_truck_two, route_truck_three):
    miles_truck_one = get_miles_closest_delivery_in_route(delivery, route_truck_one)
    miles_truck_two = get_miles_closest_delivery_in_route(delivery, route_truck_two)
    miles_truck_three = get_miles_closest_delivery_in_route(delivery, route_truck_three)

    min_val = min(miles_truck_one, miles_truck_two, miles_truck_three)
    if min_val == miles_truck_one:
        return route_truck_one
    if min_val == miles_truck_two:
        return route_truck_one
    if min_val == miles_truck_three:
        return route_truck_one
