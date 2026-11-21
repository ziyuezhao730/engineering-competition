import socket
import json
import optimization
import solarfailure
import gridfailure

HOST = "127.0.0.1"
PORT = 8800

# setup battery charge
battery = 0

# setup usable battery, ie, battery failure means usable is false
usableBattery = False

# battery charge that cannot be used right now but can be used next
buffer = 0

# function that manages battery. Keep battery charged at all times
def set_up_battery(event, next_event, cost):
    # charges the battery even if battery fails right now
    if (buffer != 0 and event != "generator_failure"):
        battery = (battery + buffer) % 101
        buffer = 0
    if (battery == 0):
        if (event != "generator_failure"):
            buffer = 100
        usableBattery = False 
    elif (battery < 100):
        if (event != "generator_failure"):
            buffer = 100 - battery
        # usableBattery = True, for safety reasons, we will never use our battery
        usableBattery = False # comment out this line if we want to prioritize lowering cost more
    elif (battery == 100):
        # usableBattery = True, for safety reasons, we will never use our battery
        usableBattery = False # comment out this line if we want to prioritize lowering cost more
    if (event == "battery_failure"):
        usableBattery = False
        return
    if (next_event == "grid_failure"):
        usableBattery = False
    if (event != "grid_faliure" and cost <= 1):
        usableBattery = False


# Testing connections - not expected anything crazy just make a baseline and hopefully it works
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    # runs for 24 hours
    for i in range(24):
        # get the message first
        rawResponse = client.recv(4096)
        response = json.loads(rawResponse.decode('utf-8'))

        # charged battery @ first hour, emergency use
        if i > 0: 
            battery = 100
            usableBattery = True

        # the answer for each input
        electricityPlan = []

        # assign total charge for solar to be split between buildings
        solar = 200

        # ignore forecast for this sample - this is for future    
        forecast = response["forecast"]

        # track how much grid is used
        gridUsage = 0

        # checks if there is a grid failure
        gridFailure = False

        # check if cloudy, if cloudy then no solar can be used
        if (response["random_event"] == "cloudy_weather"):
            solar = 0

        # when generator failure, avoid using battery so just in case grid fail next time
        if (response["random_event"] == "generator_failure"):
            usableBattery = False

        # when battery failure, can't use battery
        if (response["random_event"] == "battery_failure"):
            usableBattery = False

        # grid failure
        if (response["random_event"] == "grid_failure"):
            gridFailure = True

        # set cost to the grid price for the current hour
        cost = response["grid_cost"]

        # create dictionary for the output message
        message = {"buildings": [], "generator": 0}

        optimization.set_up_battery(response["random_event"], forecast, cost)
        message["buildings"] = optimization.plan(response["loads"], response["random_event"], forecast, cost)
        
        # for j, i in enumerate(response["loads"]):
        #     building = i["type"]

        #     # Use available resources to allocate to each building

        #     # No Failure

        #     # Solar Failure
        #     if response["random_event"] == "cloudy_weather":
        #         solar_usage = 0
        #         battery_usage, grid_usage = solarfailure.check_solar(battery, i)
            
        #     elif response["random_event"] == "grid_failure":
        #         grid_usage = 0
        #         solar_usage, battery_usage = gridfailure.check_grid(battery, i)

        #     elif response["random_event"] == "battery_failure":
        #         # battery_failure()
        #         pass
        
        #     else:
        #         # regular
        #         pass        

        #     solar -= solar_usage
        #     battery -= battery_usage
        #     message["buildings"].append({"solar": solar_usage, "battery": battery_usage, "grid": grid_usage})

        message["generator"] = 100 - battery if (not response["random_event"] == "generator_failure") else 0

        # jsonify the message dictionary and encode it to be sent as output
        data = json.dumps(message).encode('utf-8')
        client.sendall(data)
    
