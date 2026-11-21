import socket
import json
import optimization

HOST = "127.0.0.1"
PORT = 8800

# setup battery charge
battery = 0

# setup usable battery, ie, battery failure means usable is false
usableBattery = False

# battery charge that cannot be used right now but can be used next
buffer = 0

# function that manages battery. Keep battery charged at all times
def set_up_battery(event, cost):
    global battery, usableBattery, buffer
    # the charge the generator added last hour becomes usable now
    if (buffer != 0):
        battery = min(100, battery + buffer)
        buffer = 0
    if (battery == 0):
        usableBattery = False
    elif (battery < 100):
        # usableBattery = True, for safety reasons, we will never use our battery
        usableBattery = False # comment out this line if we want to prioritize lowering cost more
    elif (battery == 100):
        # usableBattery = True, for safety reasons, we will never use our battery
        usableBattery = False # comment out this line if we want to prioritize lowering cost more
    if (event == "battery_failure"):
        usableBattery = False
        return
    if (event != "grid_failure" and cost <= 1):
        usableBattery = False


# Testing connections - not expected anything crazy just make a baseline and hopefully it works
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    # runs for 24 hours
    for i in range(24):
        # get the message first
        rawResponse = client.recv(4096)
        response = json.loads(rawResponse.decode('utf-8'))

        # battery is allowed by default; the checks below and set_up_battery() can rule it out
        usableBattery = True

        # the answer for each input
        electricityPlan = []

        # assign total charge for solar to be split between buildings
        solar = 200

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

        set_up_battery(response["random_event"], cost)
        message["buildings"] = optimization.plan(response["loads"], response["random_event"], cost, battery, usableBattery)
        

        # take out what the buildings drew from the battery this hour
        battery -= sum(b["battery"] for b in message["buildings"])

        # generator tops the battery back up to 100; that charge is usable next hour
        message["generator"] = 100 - battery if (not response["random_event"] == "generator_failure") else 0
        buffer = message["generator"]

        # jsonify the message dictionary and encode it to be sent as output
        data = json.dumps(message).encode('utf-8')
        client.sendall(data)
    
