def check_solar(battery, load, cost):
    if (cost <= 1):
        return {"solar": 0, "battery": 0, "grid": grid}

    demand = building["load"]
    battery_used = min(battery, demand)
    grid = demand - battery_used
    return {"solar": 0, "battery": battery_used, "grid": grid}
    
