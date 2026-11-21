import socket
import json
import optimization
import solarfailure

HOST = "127.0.0.1"
PORT = 8800

# setup battery charge
battery = 0

# setup usable battery, ie, battery failure means usable is false
usableBattery = False

# battery charge that cannot be used right now but can be used next
buffer = 0


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

        message = {"buildings": [], "generator": 0}
        optimization.set_up_battery(response["random_event"], forecast)
        message["buildings"] = optimization.plan(response["loads"], response["random_event"], forecast, response["grid_cost"])
        
        for j, i in enumerate(response["loads"]):
            building = i["type"]

            # Use available resources to allocate to each building

            # No Failure

            # Solar Failure
            if response["random_event"] == "cloudy_weather":
                # solar_failure()
                pass
            
            elif response["random_event"] == "grid_failure":
                # grid_failure()
                pass

            elif response["random_event"] == "battery_failure":
                # battery_failure()
                pass
            # Generator Failure

            # Battery Failure

            # Grid Failure
        
            else:
                # regular
                pass        
            
            message["buildings"].append({"solar": 0, "battery": 0, "grid": i["load"]})

            if response["random_event"] == "cloudy_weather":
                    message["buildings"], battery = solarfailure.check_solar(
                battery, response["loads"]
            )
            else:
                for building in response["loads"]:
                    message["buildings"].append({
                        "solar": 0,
                        "battery": 0,
                        "grid": building["load"]
                    })

        message["generator"] = 100 - battery if (not response["random_event"] == "generator_failure") else 0
        
        data = json.dumps(message).encode('utf-8')
        client.sendall(data)
    
