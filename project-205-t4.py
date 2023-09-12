import glob
import os
import sys
import argparse
import random
import time
import carla

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

actor_list = []

def main(arg):
    """Main function of the script"""
    try:
        # Initialize the CARLA client and connect to the CARLA server
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        # Get the CARLA world
        world = client.get_world()

        # Define blueprint for the vehicle model (you need to specify this)
        vehicle_bp = None  # Replace with the actual vehicle blueprint

        # Define a transform for the vehicle's initial location and rotation (you need to specify this)
        vehicle_transform = None  # Replace with the actual transform

        # Spawn a vehicle actor in the CARLA simulation
        vehicle = world.spawn_actor(vehicle_bp, vehicle_transform)

        # Set the vehicle to autopilot
        vehicle.set_autopilot(True)

        # Adjust the spectator camera's position and rotation
        spectator_transform = carla.Transform(vehicle_transform.location, vehicle_transform.rotation)
        spectator_transform.location += vehicle_transform.get_forward_vector() * 20
        spectator_transform.rotation.yaw += 180
        spectator = world.get_spectator()
        spectator.set_transform(spectator_transform)

        # Add the spawned vehicle actor to the actor_list
        actor_list.append(vehicle)

        # Sleep for a specified time (e.g., 1 second)
        time.sleep(1.0)

    finally:
        print('Destroying actors')
        for actor in actor_list:
            actor.destroy()
        print('Done.')

# Call the main function with some argument (you can replace this with actual arguments)
if __name__ == "__main__":
    main(None)
