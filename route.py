from datetime import datetime, timedelta
from location import Location
import config as cfg
from distance import (
    get_distance,
    get_miles_of_delivery_route,
    get_miles_of_location_route
)
from delivery import Delivery


class Route:
    """
    The Route Object is a sorted list of Locations
    which is optimized for the Truck to follow to disburse Deliveries
    """
    starting_location: Location
    _miles_driven = 0
    _departure_time = None

    def __init__(self):
        self.deliveries = []
        self.starting_location = cfg.starting_location
        self._route = []
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
        return get_miles_of_delivery_route(self.starting_location, self.deliveries)

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

    def add_deliveries(self, truck_id, deliveries_list):
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
        current_location_idx = self._route.index(self._current_location)
        return get_miles_of_location_route(self._route[current_location_idx:])

    def added_distance(self, delivery_start_time, delivery_to_measure: Delivery):
        """
        Complexity: Big O(n)
        Calculate HOw many miles would be added if appending this delivery to this route
        """
        if len(self.deliveries) == 0:
            distance = get_distance(self.starting_location.address, delivery_to_measure.location.address)
            delivery_ETA = get_ETA(delivery_start_time, [delivery_to_measure]).time()
            if delivery_to_measure.earliest_deadline() > delivery_ETA:
                return distance, 0

        min_distance = None
        add_index = None
        for index in range(0, len(self.deliveries) + 1):
            deliveries_copy = self.deliveries.copy()
            deliveries_copy.insert(index, delivery_to_measure)
            added_distance_for_delivery = get_miles_of_delivery_route(self.starting_location, deliveries_copy)
            checks_pass = check_all_deliveries_arrive_by_deadline(delivery_start_time, deliveries_copy)
            if checks_pass is False:
                continue
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

    def get_miles_to_location(self, location):
        """
        Complexity: Big O(n)
        return the amount of miles to a specified location
        """
        if location is self.starting_location:
            return 0

        try:
            end_location = self._route.index(location)
        except ValueError:
            print('Location not in route')
            return

        miles_to_location = 0
        for loc_idx, location_iter in enumerate(self._route[:end_location]):
            if loc_idx == len(self._route[:end_location]):
                miles_to_location += get_distance(location_iter.address, location.address)
            miles_to_location += get_distance(location_iter.address, self._route[loc_idx + 1].address)
        return round(miles_to_location, 2)

    def get_miles_to_next_location(self):
        """
        Complexity: Big O(n)
        return the amount of miles to the next delivery location
        """
        next_location = self.get_next_location()
        if next_location is None:
            return None
        return get_distance(self._current_location.address, next_location.address)

    def miles_traveled_time_delivered(self, miles):
        """
        Complexity: Big O(1)
        Calculate when a delivery was delivered by how many miles were traveled
        """
        minutes_to_add = miles_to_minutes(miles)
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

    def populate_ETA(self, departure_time):
        """
        Complexity: Big O(n)
        """
        for delivery in self.deliveries:
            miles_to_location = self.get_miles_to_location(delivery.location)
            minutes_from_departure = miles_to_minutes(miles_to_location)
            ETA_DATETIME = datetime.combine(datetime.today(), departure_time) + timedelta(minutes=minutes_from_departure)
            ETA = ETA_DATETIME.time()
            delivery.set_ETA(ETA)

    def get_ETA_back_at_depot(self):
        """
        Complexity: Big O(1)
        """
        last_delivery = self.deliveries[-1]
        miles_to_deport_from_last_location = get_distance(last_delivery.location.address, self.starting_location.address)
        minutes_to_depot_from_last_location = miles_to_minutes(miles_to_deport_from_last_location)
        return (datetime.combine(datetime.today(), last_delivery.ETA) + timedelta(minutes=minutes_to_depot_from_last_location)).time()

    def advance_by_miles(self, new_miles_driven):
        """
        Complexity: Big O(n)
        Move the route forward the amount of the new miles driven.
        """
        print(f'have driven a total of {self._miles_driven} miles')
        # if there is no next delivery we have completed our route
        if self.get_next_delivery() is None:
            self._current_location = self.deliveries[-1].location
            self.route_complete = True

        while self.get_next_delivery():
            miles_driven_to_current_location = self.get_miles_to_location(self._current_location)

            # if we are not in the starting point
            unused_miles_driven = self._miles_driven - miles_driven_to_current_location

            print(f'driven {miles_driven_to_current_location} miles from starting point')
            # Get the next delivery and the distance from here to there.
            next_delivery = self.get_next_delivery()
            drive_distance = get_distance(self._current_location.address, next_delivery.location.address)

            # if we drove less miles than the distance to the next delivery
            # Break since we haven't reached our destination yet
            if self._miles_driven < miles_driven_to_current_location + drive_distance:
                break

            total_miles_to_next_location = miles_driven_to_current_location + drive_distance
            timestamp = self.miles_traveled_time_delivered(total_miles_to_next_location)
            next_delivery.mark_as_delivered(timestamp)
            self._current_location = next_delivery.location
            miles_driven_to_current_location += drive_distance

        if self.get_next_delivery() is None:
            self._current_location = self.deliveries[-1].location
            self.route_complete = True

        self._miles_driven += new_miles_driven


def check_all_deliveries_arrive_by_deadline(start_time, delivery_list):
    checks_pass = True
    for delivery_idx, delivery in enumerate(delivery_list):
        delivery_ETA = get_ETA(start_time, delivery_list[:delivery_idx + 1]).time()
        if delivery.earliest_deadline() < delivery_ETA:
            checks_pass = False
    return checks_pass


def get_ETA(departure_time, route):
    """
    Complexity: Big O(n)
    """
    miles_of_route = get_miles_of_delivery_route(cfg.starting_location, route)
    minutes_of_route = miles_to_minutes(miles_of_route)
    return datetime.combine(datetime.today(), departure_time) + timedelta(minutes=minutes_of_route)


def miles_to_minutes(miles):
    """
    Complexity: Big O(1)
    Transform the amount of miles into minutes traveled
    """
    return miles / 0.3  # 18MPH / 60 mins
