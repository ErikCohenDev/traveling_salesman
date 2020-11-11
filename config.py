from datetime import datetime, time, timedelta

# Constraints
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
    # Big O(1)
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


def add_an_hour_to_global_time():
    # Big O(1)
    global app_time
    app_time = app_time.replace(hour=app_time.hour + 1)
