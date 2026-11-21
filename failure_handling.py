# cloudy day
def check_solar(battery, load, usable_battery):
    demand = load["load"]
    if not usable_battery:
        return {"solar": 0, "battery": 0, "grid": demand}

    battery_used = min(battery, demand)
    grid = demand - battery_used
    return {"solar": 0, "battery": battery_used, "grid": grid}


# grid is down: only battery and solar are left, and neither can supply more than it has
def check_grid(battery, solar, load):
    demand = load["load"]
    type = load["type"]
    if type == "lecture_hall":
        # lecture halls have no solar panels, so the battery is their only source here
        battery_used = min(battery, demand)
        solar_used = 0
    else:
        solar_used = min(solar, demand)
        battery_used = min(battery, demand - solar_used)

    return {"solar": solar_used, "battery": battery_used, "grid": 0}

def checkBattery(solar, load):
    demand = load["load"]
    solar_used = 0
    if load["type"] != "lecture_hall":
        solar_used = min(solar, demand)

    return {"solar": solar_used, "battery": 0, "grid": demand - solar_used}
