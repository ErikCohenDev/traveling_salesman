from datetime import datetime
from package import get_package_by_id
from location import get_location_by_address
from delivery import Delivery, get_delivery_from_package_id
import debug as dbg
import config as cfg


class CLI:
    running = False

    def __init__(self):
        self.running = True
        self.run()

    def show_main_menu_prompt(self):
        print(
            """
-- Menu --
Enter the Letter for the report you would like to generate:
enter a number of minutes you would like to simulate has passed e.g 15, 60 (1 hr), 120 (2 hr).
    P Packages
    D Deliveries
    R Route
    T trucks
    Q return to main menu""")

    def run(self):
        today_10_20 = datetime.today().strptime("10:20:00", "%H:%M:%S")
        time_10_20 = today_10_20.time()
        """
        Complexity: Big O(N)
        Runs an the app loop and displays menu items to the user
        """
        while self.running:
            """
            If truck1 or truck2 have returned
            and truck3 is still pending, get the time the truck returned
            and dispatch the final truck
            """
            if cfg.app_time > time_10_20 and not delivery_with_wrong_address_is_fixed():
                fix_wrong_package_address(9, '410 S State St')

            if (cfg.truck1.completed_route or cfg.truck2.completed_route) and \
                    cfg.app_time > time_10_20 and cfg.truck3.started_delivering is False:

                truck_2_ETA_at_depot = cfg.truck2.get_ETA_back_at_depot()
                cfg.truck3.start_delivering(truck_2_ETA_at_depot)
                cfg.truck3.populate_ETA(truck_2_ETA_at_depot)

            self.show_main_menu_prompt()
            option = input("enter an option: ")

            """
            if the user entered an int
            fast forward the simulated clock of the app
            notify each truck how many amount of minutes have passed
            """
            try:
                if isinstance(int(option), int):
                    minutes = int(option)
                    cfg.add_minutes_to_global_time(minutes)
                    for truck in cfg.trucks:
                        if truck.started_delivering:
                            truck.minutes_passed(minutes)
                    dbg.print_current_time()
                    dbg.print_truck_table()
                    continue
            except ValueError:
                pass

            # Capitalize to cover lower case inputs
            option = option.capitalize()

            if option == "P":
                dbg.print_package_table()

            elif option == "D":
                dbg.print_delivery_table(cfg.deliveries)

            elif option == "T":
                dbg.print_truck_table()

            elif option == "R":
                dbg.print_route_table()

            elif option == "Q":
                print("Goodbye")
                self.running = False

            else:
                print("Unknown option, please enter a number from the menu\n")


def delivery_with_wrong_address_is_fixed():
    """
    Complexity: Big O(n^2)
    Check if the Delivery with the wrong address has been fixed
    Returns: bool - has it been fixed?
    """
    delivery = get_delivery_from_package_id(9)
    if delivery is None:
        return False
    return delivery.location.address == '410 S State St'


def fix_wrong_package_address(package_id, new_address):
    """
    Complexity: Big O(n^2)
    Fix the wrong package address
    update the deliveries the package is associated with
    """
    print('==================================================')
    print(f'correcting wrong address for package {package_id}')
    print('==================================================')
    correct_location = get_location_by_address(new_address)
    package_with_wrong_location = get_package_by_id(package_id)
    # Create a new delivery
    package_with_correct_address = package_with_wrong_location.update_location(correct_location)
    new_delivery = Delivery(correct_location, [package_with_correct_address])
    cfg.deliveries.append(new_delivery)
    cfg.truck3.assign_delivery(new_delivery, 0)
