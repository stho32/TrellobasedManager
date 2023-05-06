import random

from output_utils import clear_console


def select_random_task(tasks):
    return random.choice(tasks)


def print_task(task, next_time):
    clear_console()
    print("\nYour task for the next hour:")
    print("===================================")
    print(f"{task['name']}")
    print("===================================")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Next task at: {next_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
