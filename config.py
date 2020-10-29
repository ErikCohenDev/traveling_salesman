# Constraints
packages_that_must_be_on_truck_2 = [3, 18, 36, 38]  # 29.4 miles
packages_that_must_go_together = [13, 14, 15, 16, 19, 20]  # 29.8 miles
packages_that_leave_at_9_05 = [6, 25, 28, 32]  # 20.5 miles
packages_that_leave_at_10_20 = [9]  # 7.6 miles


def init(
    init_locations,
    init_distances,
    init_packages,
):
    global locations, distances, packages, deliveries, routes, trucks, starting_location
    locations = init_locations
    distances = init_distances
    packages = init_packages
    deliveries = []
    routes = []
    trucks = []
    starting_location = init_locations[0]
