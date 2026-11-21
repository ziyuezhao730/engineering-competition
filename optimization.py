from failure_handling import check_solar, check_grid, checkBattery

# in case of no event happening
def no_event(battery, next_event, solar, cost, load):
    demand = load["load"]
    type = load["type"]
    bt_used = 0
    grid_used = 0
    solar_used = 0
    # use battery if only generator can be charged next and grid is more expensive
    if (next_event != "grid_failure" and next_event != "generator_failure" and cost > 1):
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
        solar_used = min(demand, solar)
        demand -= solar_used
        grid_used = demand
        
    return {"solar": solar_used, "battery": bt_used, "grid": grid_used}


# assigns power
def plan(demands, event, next_event, cost):
    power_usage = []
    lecture = 0
    non_lecture = 0 
    power = {}
    solar = 200
    battery = 100
    # calls other functions in case of failures
    for idx, demand in enumerate(demands):
        if (demand["type"] == "lecture_hall"):
            lecture += demand["load"]
        else:
            non_lecture += demand["load"]
        if (event == "cloudy_weather"):
            power = check_solar(battery, demand)
            battery -= power["battery"]
        elif (event == "grid_failure"):
            power = check_grid(battery, solar, demand)
            battery -= power["battery"]
            solar -= power["solar"]
        elif (event == "battery_failure"):
            power = checkBattery(solar, demand)
            solar -= power["solar"]
        else: 
            power = no_event(battery, next_event, solar, cost, demand)
            battery -= power["battery"]
            solar -= power["solar"]

        power_usage.append(power)
        
    return power_usage
