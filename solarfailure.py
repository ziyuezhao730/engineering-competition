def check_solar(battery, loads):
    buildings = []

    for building in loads:
        demand = building["load"]
        battery_used = min(battery, demand)
        grid = demand - battery_used
    return battery_used, grid