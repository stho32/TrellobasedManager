import argparse
from datetime import datetime, timedelta, time
from time import sleep
from cleaning_up import cleanup
from performing_tasks import perform_work
from configuration import load_config
from simple_mode import simple_mode
from sms_interface import (
    send_sms,
)
from trello_utils import (
    get_board_id,
    get_random_task,
    check_task_exists,
    get_task_by_name,
    get_tasks,
    move_card, get_list_id, rename_task
)

def time_within_range(start, end, now=None):
    now_time = now or datetime.now().time()

    if start <= end:
        return start <= now_time <= end
    else:  # Over midnight
        return start <= now_time or now_time <= end

def rename_task_if_about_time(config, specified_time, old_name, new_name):
    # Get current time
    now = datetime.now().time()

    # Define "about time" as within 5 minutes of the specified time
    lower_bound = (datetime.combine(datetime.today(), specified_time) - timedelta(minutes=5)).time()
    upper_bound = (datetime.combine(datetime.today(), specified_time) + timedelta(minutes=5)).time()

    # Check if it is "about time"
    if time_within_range(lower_bound, upper_bound, now):
        # Check if the task exists with the old name
        if check_task_exists(config, old_name):
            task = get_task_by_name(config, old_name)
            if task['name'] == old_name:
                rename_task(config, task['id'], new_name)  # Update the task name
                print(f"Renamed task from {old_name} to {new_name}")


def send_sms_with_task(config):
    while check_task_exists(config, "Pause SMS"):  # Check for pause task
        rename_task_if_about_time(config, time(7, 0), "Pause SMS", "Pause SMSx")
        rename_task_if_about_time(config, time(17, 0), "Pause SMS", "Pause SMSx")
        print("Pause task found, waiting for 60 seconds...")
        sleep(60)  # Wait for 60 seconds

    all_tasks = get_tasks(config, config["done_list_name"])
    limit = 1
    we_have_enough_tasks = len(all_tasks) >= limit
    if we_have_enough_tasks:
        print(f"There are already a lot of tasks in the pipeline, not pushing more for now.")
        return

    task = get_random_task(config, config["list_name"])

    token_id = config["SIPGATE_TOKENID"]
    token = config["SIPGATE_TOKEN"]
    recipient = config["SMS_RECEIPIENT"]

    # Add current date and time to message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Please work on the task: {task['name']}. Time sent: {current_time}"

    print(f"Sending message: {message}")  # Log the message to the screen

    send_sms(token_id, token, recipient, message)

    # Get the id of the "done_list"
    board_id = get_board_id(config, config["board_name"])
    done_list_id = get_list_id(config, board_id, config['done_list_name'])

    # Move the task to the "done_list"
    move_card(config, task['id'], done_list_id)



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
    parser.add_argument(
        "--list-name",
        type=str,
        help="Specify the name of the list to perform tasks on, only used with --perform flag.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=999,
        help="Specify the number of rounds to perform tasks, only used with --perform flag.",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Specify this flag to start the program in simple mode.",
    )
    parser.add_argument(
        "--sms",
        action="store_true",
        help="Specify this flag to send an SMS.",
    )

    args = parser.parse_args()

    config = load_config()

    list_name = args.list_name
    if args.list_name is None:
        list_name = config["list_name"]

    if args.perform:
        perform_work(config, args, list_name, args.rounds)
    elif args.cleanup:
        cleanup(config, args)
    elif args.simple:
        simple_mode(config, list_name)
    elif args.sms:
        while True:  # Create an infinite loop
            send_sms_with_task(config)
            sleep(60)
    else:
        print(
            "Neither the perform, cleanup, simple, nor sms flag was set, exiting program."
        )
        exit()


if __name__ == "__main__":
    main()
