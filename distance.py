from location import Location
from typing import List
from delivery import Delivery
import config as cfg


def get_distance(address_start, address_end):
    # Big O(1)
    """
    ### Parameters
    1. address_start: str
        - the initial location to compare two
    2. address_end : str
        - the second address to compare to
    ### Returns
    - number
        - The distance in miles from
        address_start to address_end
    - None
        - The distance could not be calculates
        from the data in the distances Hashmap
    """
    if address_start == address_end:
        return 0
    if (address_start in cfg.distances) and (
        address_end in cfg.distances[address_start]
    ):
        return cfg.distances[address_start][address_end]
    if (address_end in cfg.distances) and (address_start in cfg.distances[address_end]):
        return cfg.distances[address_end][address_start]
    return None


def get_closest_next_location(current_address, pending_deliveries):
    # Big O(n)
    distance_to_next_location = None
    for next_delivery_address in pending_deliveries:
        next_location_distance = distance_to_next_location
        calculated_distance = get_distance(current_address, next_delivery_address.location.address)
        if (
            next_location_distance is None or next_location_distance > calculated_distance
        ):
            distance_to_next_location = (next_delivery_address, calculated_distance)
    return distance_to_next_location


def get_miles_of_route(starting_location: Location, delivery_list, return_to_depot=False):
    # Big O(n)
    """
    ### Parameters
    1. delivery_list: List[Delivery]
        - the delivery list for the route
    ### Returns
    - number
        - the number of miles that route sums up to
    """
    total_miles = 0
    for index, delivery in enumerate(delivery_list):
        origin = None
        if index == 0:
            origin = starting_location.address
        else:
            origin = delivery_list[index - 1].location.address
        dest = delivery.location.address
        new_miles = get_distance(origin, dest)
        total_miles += new_miles
    if return_to_depot:
        return_to_depot_distance = get_distance(delivery_list[-1].location.address, starting_location.address)
        total_miles += return_to_depot_distance
    return total_miles
