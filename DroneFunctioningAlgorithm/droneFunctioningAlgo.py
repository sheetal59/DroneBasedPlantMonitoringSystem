from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from collections.abc import MutableMapping


# Connect to the drone
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# Arm and takeoff function
def arm_and_takeoff(target_altitude):
    print("Pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(f" Altitude: {vehicle.location.global_relative_frame.alt}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Navigate to a location
def goto_location(lat, lon, alt):
    location = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(location)

# Example Usage
arm_and_takeoff(10)  # Takeoff to 10 meters
goto_location(35.363261, 149.165230, 10)  # Navigate to coordinates
time.sleep(10)  # Hover for 10 seconds

# Return to Launch
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")
vehicle.close()
