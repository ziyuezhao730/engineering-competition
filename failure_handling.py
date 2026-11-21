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
    solar_used = 0
    battery_used = 0
    if type == "lecture_hall":
        battery_used = load
    elif solar >= load:
        solar_used = load
    else:
        solar_used = solar
        battery_used = load - solar
        
    return {"solar": solar_used, "battery": battery_used, "grid": 0}

def checkBattery(demand, grid, solar):
    if building["type"] == "lecture_hall":
        grid += demand
    else:
        if solar < demand:
            solar = 0
            grid += demand - solar
        else:
            solar -= demand

    return {"solar": solar_used, "battery": battery_used, "grid": 0}
