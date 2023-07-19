import argparse
from datetime import datetime
import time
from cleaning_up import cleanup
from performing_tasks import perform_work
from configuration import load_config
from simple_mode import simple_mode
from sms_interface import (
    send_sms,
)
from trello_utils import (
    get_random_task,
    check_task_exists,
)  # make sure you define what simple_mode does in the simple_mode module


def send_sms_with_task(config):
    while check_task_exists(config, "Pause SMS"):  # Check for pause task
        print("Pause task found, waiting for 60 seconds...")
        time.sleep(60)  # Wait for 60 seconds

    task = get_random_task(config, config["list_name"])

    token_id = config["SIPGATE_TOKENID"]
    token = config["SIPGATE_TOKEN"]
    recipient = config["SMS_RECEIPIENT"]

    # Add current date and time to message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Please work on the task: {task['name']}. Time sent: {current_time}"

    print(f"Sending message: {message}")  # Log the message to the screen

    send_sms(token_id, token, recipient, message)


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
            time.sleep(1800)  # Pause for 1800 seconds (30 minutes)
    else:
        print(
            "Neither the perform, cleanup, simple, nor sms flag was set, exiting program."
        )
        exit()


if __name__ == "__main__":
    main()
