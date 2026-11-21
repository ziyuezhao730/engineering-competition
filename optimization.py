from solarfailure import check_solar
from main import usableBattery

# assigns power
def plan(demands, event, next_event, cost):
    power_usage = []
    lecture = 0
    non_lecture = 0 
    cost = 0
    # calls other functions in case of failures
    for idx, demand in enumerate(demands):
        if (demand["type"] == "lecture_hall"):
            lecture += demand["load"]
        else:
            non_lecture += demand["load"]
        if (event == "cloudy_weather"):
            if not usableBattery:
                power = check_solar(0, demand, cost)
            else:
                power = check_solar(battery, demand, cost)
        
        power_usage.append(power)

# function that manages battery. Keep battery charged at all times
def set_up_battery(event, next_event):
    if (buffer != 0 and event != "generator_failure"):
        battery = (battery + buffer) % 101
        buffer = 0
    if (battery == 0):
        if (event != "generator_failure"):
            buffer = 100
        usableBattery = False 
    else if (battery < 100):
        if (event != "generator_failure"):
            buffer = 100 - battery
        usabeBattery = True
    else if (battery == 100):
        usableBattery = True
    if (next_event == "grid_failure"):
        usableBattery = False

