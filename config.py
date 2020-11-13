from datetime import datetime, time, timedelta

"""
Define Lists of package ID's which have restrictions
"""
packages_that_must_be_on_truck_2 = [3, 18, 36, 38]  # 29.4 miles
packages_that_must_go_together = [13, 14, 15, 16, 19, 20]  # 29.8 miles
packages_that_leave_at_9_05 = [6, 25, 28, 32]  # 20.5 miles
packages_that_leave_at_10_20 = [9]  # 7.6 miles
packages_restrictions = [
    *packages_that_must_be_on_truck_2,
    *packages_that_must_go_together,
    *packages_that_leave_at_9_05,
    *packages_that_leave_at_10_20
]


def init(
    init_locations,
    init_distances,
    init_packages,
):
    """
    Complexity: Big O(1)
    Initializer function to declare all the global variables needed during the applications lifetime
    """
    global locations, distances, packages, deliveries, routes, trucks, starting_location, day_start, app_time, total_miles_driven_by_all_trucks
    locations = init_locations
    distances = init_distances
    packages = init_packages
    deliveries = []
    routes = []
    trucks = []
    starting_location = init_locations[0]
    day_start = datetime.today().strptime("08:00:00", "%H:%M:%S")
    app_time = day_start.time()
    total_miles_driven_by_all_trucks = 0


def add_minutes_to_global_time(minutes):
    """
    Complexity: Big O(1)
    Simulate that amount of minutes have passed
    """
    global app_time
    new_minutes = minutes + app_time.minute
    new_hours = app_time.hour
    if (new_minutes >= 60):
        new_hours = (new_minutes // 60) + app_time.hour
        new_minutes = new_minutes % 60

    app_time = app_time.replace(minute=new_minutes, hour=new_hours)
