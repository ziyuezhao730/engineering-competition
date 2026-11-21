def check_solar(battery, loads):
    buildings = []

    for building in loads:
        demand = building["load"]
        battery_used = min(battery, demand)
        battery -= battery_used

        buildings.append({
            "solar": 0,
            "battery": battery_used,
            "grid": demand - battery_used
        })

    return battery, buildings