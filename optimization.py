import solarfailure.py

# assigns power
def plan(demands, event, next_event, grid_price):
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
                power = check_solar(0)
            else:
                power = check_solar(battery)
        
        power_usage.append({"solar": 0, "battery": 0, "grid": demand["load"]})

# function that manages battery. Keep battery charged at all times
def set_up_battery(event, next_event):
    if (buffer != 0):
        battery += buffer
        buffer = 0
    if (battery == 0):
        buffer = 100
        usableBattery = False
        return 
    if (battery < 100):
        buffer = 100 - battery
        usabeBattery = True
        return
    if (battery == 100):
        usableBattery = True
