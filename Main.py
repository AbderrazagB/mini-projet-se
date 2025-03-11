import threading
import time
import random
import os

# Shared resource: Warehouse shelf
shelf_available = True  # Indicates whether the shelf is available
current_robot = None  # Tracks which robot is using the shelf

# Lock for synchronization
lock = threading.Lock()

# Number of robots
NUM_ROBOTS = 5

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red(text):
    print(f"\033[91m{text}\033[0m")  # ANSI escape code for red text

def access_shelf_without_lock(robot_id):
    global shelf_available, current_robot

    print(f"[Robot {robot_id}] is moving towards the shelf...")
    time.sleep(random.uniform(0.5, 1.0))  # Simulate travel time

    if shelf_available:
        print(f"[Robot {robot_id}] is accessing the shelf...")
        shelf_available = False
        current_robot = robot_id
        time.sleep(random.uniform(1.0, 2.0))  # Simulate item pickup time
        shelf_available = True
        current_robot = None
        print(f"[Robot {robot_id}] has finished picking an item.")
    else:
        print_red(f"[CRASH] Robot {robot_id} collided with Robot {current_robot}!")

def access_shelf_with_lock(robot_id):
    """ Robots accessing the shelf with synchronization (no conflicts). """
    global shelf_available, current_robot

    print(f"[Robot {robot_id}] is moving towards the shelf...")
    time.sleep(random.uniform(0.5, 1.0))  # Simulate travel time

    with lock:  # Ensures only one robot accesses the shelf at a time
        print(f"[Robot {robot_id}] is accessing the shelf...")
        shelf_available = False  # Shelf is occupied
        current_robot = robot_id
        time.sleep(random.uniform(1.0, 2.0))  # Simulate item pickup time
        shelf_available = True  # Shelf is now free
        current_robot = None
        print(f"[Robot {robot_id}] has finished picking an item.")

def run_simulation(target_function):
    """ Starts multiple robot threads trying to access the shelf. """
    threads = []

    for robot_id in range(NUM_ROBOTS):
        thread = threading.Thread(target=target_function, args=(robot_id,))
        thread.start()
        threads.append(thread)
        time.sleep(0.2)  # Small delay to make execution more visible

    for thread in threads:
        thread.join()

    input("\nPress any key to return to the main menu...")

def main():
    while True:
        clear_screen()
        print("\n=== Warehouse Robot Simulation ===")
        print("1. Run WITHOUT synchronization (robots may conflict)")
        print("2. Run WITH synchronization (robots take turns)")
        print("3. Exit")
        choice = input("\nChoose an option (1, 2, or 3): ")

        if choice == "1":
            clear_screen()
            print("\nRunning WITHOUT synchronization (Conflicts Expected)")
            run_simulation(access_shelf_without_lock)
        elif choice == "2":
            clear_screen()
            print("\nRunning WITH synchronization (No Conflicts)")
            run_simulation(access_shelf_with_lock)
        elif choice == "3":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter 1, 2, or 3.")
            time.sleep(1)

if __name__ == "__main__":
    main()
