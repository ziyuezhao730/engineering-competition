def checkBattery(loads, grid, solar):
    for building in loads:
        demand = building["load"]
        if building["type"] == "lecture_hall":
            grid += demand
        else:
            if solar < demand:
                solar = 0
                grid += demand - solar
            else:
                solar -= demand

    return [grid, solar]
