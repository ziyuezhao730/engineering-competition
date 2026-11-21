from main import usableBattery

def check_solar(battery, load):
    demand = load["load"]
    if not usableBattery:
        return {"solar": 0, "battery": 0, "grid": demand}

    battery_used = min(battery, demand)
    grid = demand - battery_used
    return {"solar": 0, "battery": battery_used, "grid": grid}


def check_grid(battery, solar, load):
    demand = load["load"]
    type = load["type"]
    solar_used = 0
    battery_used = 0
    if type == "lecture_hall":
        battery_used = demand
    elif solar >= load["load"]:
        solar_used = demand
    else:
        solar_used = solar
        battery_used = demand - solar
        
    return {"solar": solar_used, "battery": battery_used, "grid": 0}

def checkBattery(solar, load):
    grid = 0
    if load["type"] == "lecture_hall":
        grid += load["load"]
    else:
        if solar < load["load"]:
            solar = 0
            grid += load["load"] - solar
        else:
            solar -= load["load"]

    return {"solar": solar_used, "battery": 0, "grid": grid}
