from cli import CLI
from csv_import import load_data
from delivery import create_deliveries
import config as cfg
from truck import distribute_deliveries_to_trucks


def init_data():
    """'
    Big O(n^2)
    Load up all the data from the data folder instantiate the Objects for each
    and store it in the config module to be available globally
    """
    # Get the Data
    init_locations, init_distances, init_packages = load_data()

    # Save to global variables to make easily accessible
    cfg.init(init_locations, init_distances, init_packages)

    # Create deliveries of packages to specific locations
    deliveries = create_deliveries()
    cfg.deliveries = deliveries


def assign_deliveries():
    """'
    Create Routes from pending devlieries and
    Assign deliveries to all the available trucks
    """
    # get and distrubute deliveries without restrictions to available trucks
    distribute_deliveries_to_trucks()
    cfg.truck1.start_delivering(cfg.app_time)
    cfg.truck2.start_delivering(cfg.app_time)

    cfg.truck1.populate_ETA(cfg.app_time)
    cfg.truck2.populate_ETA(cfg.app_time)


def main():
    """'
    Big O(n^3)
    Initiate the application
    """
    init_data()
    assign_deliveries()
    CLI().run()


if __name__ == "__main__":
    main()
