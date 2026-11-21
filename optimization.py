from failure_handling import check_solar, check_grid, check_battery
from main import usableBattery, battery, buffer

# assigns power
def plan(demands, event, next_event, cost):
    power_usage = []
    lecture = 0
    non_lecture = 0 
    cost = 0
    power = {}
    # calls other functions in case of failures
    for idx, demand in enumerate(demands):
        if (demand["type"] == "lecture_hall"):
            lecture += demand["load"]
        else:
            non_lecture += demand["load"]
        if (event == "cloudy_weather"):
            power = check_solar(battery, demand)
        elif (event == "gridfailure"):
            power = check_grid(battery, demand)
        elif (event == "batteryfailure"):
        else: 
        power_usage.append(power)
        
    return power_usage

# function that manages battery. Keep battery charged at all times
def set_up_battery(event, next_event, cost):
    # charges the battery even if battery fails right now
    if (buffer != 0 and event != "generator_failure"):
        battery = (battery + buffer) % 101
        buffer = 0
    if (battery == 0):
        if (event != "generator_failure"):
            buffer = 100
        usableBattery = False 
    elif (battery < 100):
        if (event != "generator_failure"):
            buffer = 100 - battery
        # usableBattery = True, for safety reasons, we will never use our battery
        usableBattery = False # comment out this line if we want to prioritize lowering cost more
    elif (battery == 100):
        # usableBattery = True, for safety reasons, we will never use our battery
        usableBattery = False # comment out this line if we want to prioritize lowering cost more
    if (event == "battery_failure"):
        usableBattery = False
        return
    if (next_event == "grid_failure"):
        usableBattery = False
    if (event != "grid_faliure" and cost <= 1):
        usableBattery = False

