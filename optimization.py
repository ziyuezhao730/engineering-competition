def plan(demands, event, next_event, grid_price):
  power_usage = []
  lecture = 0
  non_lecture = 0 
  cost = 0
  # NOT optimized AT ALL - use all grid
  for idx, demand in enumerate(demands):
      if (demand["type"] == "lecture_hall"):
          lecture += demand["load"]
      else:
          non_lecture += demand["load"]
      power_usage.append({"solar": 0, "battery": 0, "grid": demand["load"]})
