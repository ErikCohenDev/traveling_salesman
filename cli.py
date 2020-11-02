import debug as dbg


class CLI:
    running = False

    def __init__(self, packages):
        self.running = True
        self.run()

    def show_main_menu_prompt(self):
        print(
            """
--Main Menu--
    1. packages
    2. deliveries
    3. trucks
    4. quit application""")

    def show_packages_prompt(self):
        print(
            """
--Packages Menu--
    1. Show all delivered packages and their delivery times
    2. show all undelivered packages
    3. show all packages
    4. return to main menu""")

    def show_deliveries_prompt(self):
        print(
            """
--Deliveries Menu--
    1. packages
    2. deliveries
    3. trucks
    4. return to main menu"""
        )

    def show_trucks_prompt(self):
        print(
            """
--Trucks Menu--
    1. packages
    2. deliveries
    3. trucks
    4. return to main menu""")

    def run(self):
        while self.running:
            self.show_main_menu_prompt()
            option = input("enter an option: ")
            if option == "1":
                self.show_packages_prompt()
                sub_option = input("enter an option: ")
                if sub_option == "1":
                    self.display_delivered_packages()
                elif sub_option == "2":
                    self.display_undelivered_packages()
                elif sub_option == "3":
                    self.display_all_packages()

            elif option == "2":
                self.show_deliveries_prompt()
                sub_option = input("enter an option: ")

            elif option == "3":
                self.show_trucks_prompt()
                sub_option = input("enter an option: ")

            elif option == "4":
                print("Goodbye")
                self.running = False

            else:
                print("Unknown option, please enter a number from the menu\n")

    def display_delivered_packages(self):
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
