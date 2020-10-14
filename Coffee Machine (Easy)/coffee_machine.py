class CoffeeMachine:

    def __init__(self, water, milk, beans, cups, money):
        self.on = True
        self.supply = [water, milk, beans, cups, money]
        self.supply_type = ["water", "milk", "coffee beans", "cups", "money"]
        self.commands = ["buy", "fill", "take", "remaining", "exit"]
        self.espresso = [-250, 0, -16, -1, 4]
        self.latte = [-350, -75, -20, -1, 7]
        self.cappuccino = [-200, -100, -12, -1, 6]

    def input_read(self, user_input):
        if user_input == self.commands[0]:
            self.buy()
        if user_input == self.commands[1]:
            self.fill()
        if user_input == self.commands[2]:
            self.take()
        if user_input == self.commands[3]:
            self.remaining()
        if user_input == self.commands[4]:
            self.on = False

    def buy(self):
        choice = input("What do you want to buy? "
                       "1 - espresso, "
                       "2 - latte, "
                       "3 - cappuccino, "
                       "back - to main menu:")
        if choice == "1":
            if self.can_make(self.espresso):
                self.supply_change(self.espresso)
        if choice == "2":
            if self.can_make(self.latte):
                self.supply_change(self.latte)
        if choice == "3":
            if self.can_make(self.cappuccino):
                self.supply_change(self.cappuccino)

    def can_make(self, coffee_type):
        n = 0
        for supply in self.supply:
            if supply + coffee_type[n] < 0:
                print("Sorry, not enough {}".format(self.supply_type[n]))
                return False
            else:
                n += 1
        print("I have enough resources, making you a coffee!")
        return True

    def supply_change(self, coffee_type):
        n = 0
        for supply in coffee_type:
            self.supply[n] += supply
            n += 1

    def fill(self):
        self.supply[0] += int(input("Write how many ml of {} do you want to add:".format(self.supply_type[0])))
        self.supply[1] += int(input("Write how many ml of {} do you want to add:".format(self.supply_type[1])))
        self.supply[2] += int(input("Write how many ml of {} do you want to add:".format(self.supply_type[2])))
        self.supply[3] += int(input("Write how many ml of {} do you want to add:".format(self.supply_type[3])))

    def take(self):
        print("I gave you ${}".format(self.supply[4]))
        self.supply[4] = 0

    def remaining(self):
        print("The coffee machine has:\n"
              f"{self.supply[0]} of water\n"
              f"{self.supply[1]} of milk\n"
              f"{self.supply[2]} of coffee beans\n"
              f"{self.supply[3]} of disposable cups\n"
              f"${self.supply[4]} of money")


machine = CoffeeMachine(400, 540, 120, 9, 550)
while machine.on:
    machine.input_read(input("Write action (buy, fill, take, remaining, exit):"))
