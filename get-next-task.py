import random
import argparse
import time
import os
from datetime import datetime, timedelta

from trello_utils import load_config, get_tasks, get_board_id, get_list_id


def select_random_task(tasks):
    return random.choice(tasks)


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def print_task(task, next_time):
    clear_console()
    print("\nYour task for the next hour:")
    print("===================================")
    print(f"{task['name']}")
    print("===================================")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Next task at: {next_time.strftime('%Y-%m-%d %H:%M:%S')}\n")


def main():
    parser = argparse.ArgumentParser(description="Trello task selector.")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Enable loop mode to select tasks every hour.",
    )

    args = parser.parse_args()

    config = load_config()

    if args.loop:
        while True:
            tasks = get_tasks(config)

            if not tasks:
                print("No tasks found. Retrying in 1 hour.")
            else:
                random_task = select_random_task(tasks)
                next_time = datetime.now() + timedelta(hours=1)
                print_task(random_task, next_time)

            time.sleep(3600)  # Sleep for 1 hour
    else:
        tasks = get_tasks(config)

        if not tasks:
            print("No tasks found.")
            return

        random_task = select_random_task(tasks)
        next_time = datetime.now() + timedelta(hours=1)
        print_task(random_task, next_time)


if __name__ == "__main__":
    main()
