from main import usableBattery

def check_solar(battery, load):
    demand = load["load"]
    if not usableBattery:
        return {"solar": 0, "battery": 0, "grid": demand}

    battery_used = min(battery, demand)
    grid = demand - battery_used
    return {"solar": 0, "battery": battery_used, "grid": grid}
    
