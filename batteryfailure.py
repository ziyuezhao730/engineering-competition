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
