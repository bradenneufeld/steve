import time

# Agents
class Agent():
    def __init__(self):
        self.type = "Agent"
        self.name = "Untitled Agent"

    def announce(self, announcement):
        print(self.name, ": ", announcement)

class Person(Agent):
    def __init__(self, name):
        self.type = "Person"
        self.name = name
        self.cash = 10000

class Building(Agent):
    def __init__(self):
        self.type = "Building"

class ServiceBuilding(Building):
    def __init__(self, entity):
        self.subtype = "Service Building"
        self.open_public = False
        self.entity = entity

class GasStation(ServiceBuilding):
    def __init__(self, entity, gas_resource):
        super().__init__(entity)
        self.name = "Steve's Gas"
        self.resource = gas_resource
        self.inventory = {self.resource.name: 0}
        self.price_list = {self.resource.name: int(self.resource.value_wholesale*1.2)}

    def update(self):
        dollars = self.entity.cash/100
        self.announce("cash =  " + "$%.2f" % dollars + " | gas = " + str(self.inventory["gas"]))
        self.do_inventory()

    def do_inventory(self):
        if self.inventory["gas"] < 200:
            self.announce("out of gas! ordering more.")
            gas_resource.order_resource(self.entity, self, 500)
            dollars = self.entity.cash/100
            self.announce("cash =  " + "$%.2f" % dollars + " | gas = " + str(self.inventory["gas"]))


    def sell(self, volume):
        self.inventory["gas"] -= volume
        self.entity.cash += volume*self.price_list["gas"]
        dollars = volume*self.price_list["gas"]/100
        self.announce("sold  " + str(volume) + "L of " + self.resource.name + " for $%.2f" % dollars)
        dollars = self.entity.cash/100
        self.announce("cash =  " + "$%.2f" % dollars + " | gas = " + str(self.inventory["gas"]))

# Other
class Entity():
    def __init__(self, name):
        self.type = "Entity"
        self.name = name
        self.cash = 100000

# Resources
class Resource():
    def __init__(self):
        self.type = "Resource"

class VolumetricResource(Resource):
    def __init__(self, name, value_wholesale):
        self.name = name
        self.type = "Volumetric Resource"
        self.value_wholesale = value_wholesale
        self.availability_global = True

    def order_resource(self, entity, building, volume):
        if self.availability_global:
            cost = volume*self.value_wholesale
            entity.cash -= cost
            building.inventory[self.name] += volume
            dollars = cost/100
            print(entity.name, " ordered ", str(volume), "L of ", self.name, " for $%.2f" % dollars)


class WorldTime():
    def __init__(self):
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.year = 0

    def update(self, d_minutes = 1, d_hours = 0, d_days = 0, d_years = 0):
        self.minute += d_minutes
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        self.hour += d_hours
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
        self.day += d_days
        while self.hour >= 365:
            self.day -= 365
            self.year += 1
        return {"minute": self.minute, "hour": self.hour, "day": self.day, "year":self.year}

    def is_now(self, hour, minute=0, day=None, year=None):
        if day is None:
            day = self.day
        if year is None:
            year = self.year
        if hour == self.hour and minute == self.minute and day == self.day and year == self.year:
            return True
        else:
            return False


# Initialize World
gas_resource = VolumetricResource("gas", 110)
steves_gas = Entity("Steve's Gas Co")
gas_station = GasStation(steves_gas, gas_resource)
steve = Person("Steve")
world_time = WorldTime()

while True:

    current_time = world_time.update()

    if current_time['hour'] == 0 and current_time['minute'] == 0:
        time.sleep(2)
        print("------------------NEW DAY!----------------------")
    if current_time['minute'] == 0:
        print(current_time["hour"], " : ", str(current_time["minute"]), " on day ", str(current_time["day"]))
    if world_time.is_now(6):
        gas_station.open_public = True
        gas_station.update()
    if world_time.is_now(10):
        gas_station.sell(50)
    if world_time.is_now(12):
        gas_station.sell(50)
    if world_time.is_now(14):
        gas_station.sell(50)
    if world_time.is_now(16):
        gas_station.sell(50)
    if world_time.is_now(22):
        gas_station.open_public = False