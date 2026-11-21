from failure_handling import check_solar, check_grid, checkBattery

# in case of no event happening
def no_event(battery, solar, cost, load):
    demand = load["load"]
    bt_used = 0
    grid_used = 0
    solar_used = 0
    # use battery if grid is more expensive
    if (cost > 1):
        if load["type"] == "lecture_hall":
            bt_used = min(demand, battery)
            demand -= bt_used
            grid_used = demand
        else:
            solar_used = min(demand, solar)
            demand -= solar_used
            bt_used = min(demand, battery)
            demand -= bt_used
            grid_used = demand
    else:
        # lecture halls have no solar panels
        if load["type"] != "lecture_hall":
            solar_used = min(demand, solar)
            demand -= solar_used
        grid_used = demand
        
    return {"solar": solar_used, "battery": bt_used, "grid": grid_used}


# assigns power
def plan(demands, event, cost, battery, usable_battery):
    power_usage = []
    solar = 200
    # calls other functions in case of failures
    for demand in demands:
        if (event == "cloudy_weather"):
            power = check_solar(battery, demand, usable_battery)
            battery -= power["battery"]
        elif (event == "grid_failure"):
            power = check_grid(battery, solar, demand)
            battery -= power["battery"]
            solar -= power["solar"]
        elif (event == "battery_failure"):
            power = checkBattery(solar, demand)
            solar -= power["solar"]
        else: 
            power = no_event(battery, solar, cost, demand)
            battery -= power["battery"]
            solar -= power["solar"]

        power_usage.append(power)
        
    return power_usage
