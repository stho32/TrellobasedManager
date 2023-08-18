from datetime import datetime
import random

from library.output_utils import clear_console


def select_random_task(tasks):
    return random.choice(tasks)


def print_task(task, next_time, alternative_tasks=None):
    clear_console()
    print("\nYour task for the next interval:")
    print("===================================")
    print(f"")
    print(f"")
    print(f"==> {task['name']}")
    print(f"")
    print(f"")
    print("===================================")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Next task at: {next_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    if alternative_tasks:
        print("Alternative tasks:")
        print("-------------------")
        for idx, alternative_task in enumerate(alternative_tasks, start=1):
            print(f"{idx}. {alternative_task['name']}")
        print("-------------------\n")
