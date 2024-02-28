import random
import time
import threading
import socket

# Define constants
MAX_SPEED_LIMIT = 60  # mph
NUM_CARS = 20  # Number of cars in simulation
PARKING_LOT_SIZE = 10  # Number of parking spaces
UPDATE_INTERVAL = 1  # Seconds between updates

# Data structures for traffic and parking data
cars = []
parking_lot = [False] * PARKING_LOT_SIZE

# Function to generate random car data
def generate_car():
    return {
        "id": random.randint(1, 1000),
        "location": random.uniform(0, 100),  # Distance on the road
        "speed": random.randint(20, MAX_SPEED_LIMIT),  # Speed in mph
        "direction": random.choice(["north", "south"]),
        "is_looking_for_parking": random.choice([True, False]),
    }

# Function to update car data (location, speed)
def update_car(car):
    if car["direction"] == "north":
        car["location"] += car["speed"] * UPDATE_INTERVAL / 3600  # Convert mph to miles/second
    else:
        car["location"] -= car["speed"] * UPDATE_INTERVAL / 3600

    # Enforce boundary conditions
    if car["location"] >= 100:
        car["location"] = 0
        car["direction"] = "south"
    elif car["location"] <= 0:
        car["location"] = 100
        car["direction"] = "north"

    # Update speed randomly
    car["speed"] = max(20, car["speed"] + random.randint(-5, 5))  # Prevent negative speeds

# Function to handle parking requests and updates
def handle_parking(car):
    global parking_lot

    if car["is_looking_for_parking"]:
        for i in range(PARKING_LOT_SIZE):
            if not parking_lot[i]:
                # Found a free spot
                car["is_looking_for_parking"] = False
                parking_lot[i] = True
                return True

    return False

def is_occupied(i):
    return parking_lot[i]

def handle_client_requests(conn, addr):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        # Process request (e.g., get traffic data, parking availability for a specific spot)
        if data.startswith("GET_TRAFFIC"):
            response = f"Current average speed: {get_average_speed()} mph\n"
        elif data.startswith("GET_PARKING"):
            spot_number = int(data.split()[1])
            response = f"Spot {spot_number} is {'occupied' if is_occupied(spot_number) else 'free'}\n"
        else:
            response = "Invalid request\n"

        conn.sendall(response.encode())

    conn.close()

def get_average_speed():
    total_speed = 0
    for car in cars:
        total_speed += car["speed"]
    return total_speed / len(cars)

def display_traffic_data():
    global cars

    # Clear plot for visual representation
    plt.clf()

    # Plot car locations on the road
    x_values = [car["location"] for car in cars]
    speeds = [car["speed"] for car in cars]
    plt.scatter(x_values, speeds, c='blue')

    # Plot occupied parking spots
    occupied_spots = [i for i, spot in enumerate(parking_lot) if spot]
    plt.scatter(occupied_spots, [MAX_SPEED_LIMIT + 5 for _ in occupied_spots], c='red')

    # Display labels and limits
    plt.xlabel("Distance (miles)")
    plt.ylabel("Speed (mph)")
    plt.title(f"Traffic Simulation - Time: {time.strftime('%H:%M:%S')}")
    plt.xlim(0, 100)
    plt.ylim(0, MAX_SPEED_LIMIT + 10)

    plt.pause
