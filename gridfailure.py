def check_grid(battery, solar, building):
    load = building["load"]
    type = building["type"]
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