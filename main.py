import argparse
from performing_tasks import perform_work
from trello_utils import (
    delete_card,
    get_all_lists,
    get_all_tasks,
    load_config,
    move_card,
)
import random


def cleanup(config, args):
    all_tasks = get_all_tasks(config)

    if not all_tasks:
        print("No tasks found.")
        return

    all_lists = get_all_lists(config)

    if not all_lists:
        print("No lists found.")
        return

    random.shuffle(all_tasks)

    for task in all_tasks:
        print(f"\nTask: {task['name']}")

        for i, list_obj in enumerate(all_lists, start=1):
            print(f"{i}. {list_obj['name']}")

        print("d. Delete task")
        print("Press Enter to stop.\n")

        user_input = input("Choose an option: ")

        if user_input == "d":
            delete_card(config, task["id"])
        elif user_input.isdigit():
            list_index = int(user_input) - 1
            if 0 <= list_index < len(all_lists):
                move_card(config, task["id"], all_lists[list_index]["id"])
        elif user_input == "":
            break
        else:
            print("Invalid option. Skipping this task.")


def main():
    parser = argparse.ArgumentParser(description="Trello task selector.")
    parser.add_argument(
        "--work-duration",
        type=int,
        metavar="MINUTES",
        default=25,
        help="Specify the work duration in minutes for each task.",
    )
    parser.add_argument(
        "--break-duration",
        type=int,
        metavar="MINUTES",
        default=5,
        help="Specify the break duration in minutes after each task.",
    )
    parser.add_argument(
        "--perform",
        action="store_true",
        help="Specify this flag to start the work process.",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Specify this flag to start the cleanup process.",
    )

    args = parser.parse_args()

    config = load_config()

    # check if the perform flag is set
    if args.perform:
        # start the work process
        perform_work(config, args)
    elif args.cleanup:
        # start the cleanup process
        cleanup(config, args)
    else:
        print("Neither the perform nor the cleanup flag was set, exiting program.")
        exit()


if __name__ == "__main__":
    main()
