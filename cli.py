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
        """
        Complexity: Big O(N)
        Runs an the app loop and displays menu items to the user
        """
        while self.running:
            if (cfg.truck1.completed_route or cfg.truck2.completed_route) and cfg.truck3.started_delivering is False:
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

    def display_delivered_packages(self):
        """
        Big O(N)
        """
        count = 0
        for package in self.packages:
            if package.delivered:
                count += 1
                print(f"id: {len(package.id)} ; Address {package.address}")
        if count == 0:
            print("No packages have been delivered")

    def display_undelivered_packages(self):
        pass

    def display_all_packages(self):
        pass
