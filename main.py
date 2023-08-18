import argparse
from datetime import datetime, time
from time import sleep
from modes.cleanup_mode import cleanup
from modes.perform_mode import perform_work
from library.configuration import load_config
from modes.simple_mode import simple_mode
from library.sms_interface import (
    send_sms,
)
from library.trello_utils import (
    get_board_id,
    get_next_task,
    check_task_exists,
    get_tasks,
    move_card, get_list_id,
      rename_task_if_about_time
)




def send_sms_with_task(config):
    while check_task_exists(config, "Pause SMS"):  # Check for pause task
        rename_task_if_about_time(config, time(7, 0), "Pause SMS", "Pause SMSx")
        rename_task_if_about_time(config, time(17, 0), "Pause SMS", "Pause SMSx")
        print("Pause task found, waiting for 60 seconds...")
        sleep(60)  # Wait for 60 seconds

    all_tasks = get_tasks(config, config["done_list_name"])
    limit = 2
    we_have_enough_tasks = len(all_tasks) >= limit
    if we_have_enough_tasks:
        print(f"There are already a lot of tasks in the pipeline, not pushing more for now.")
        return

    task = get_next_task(config, config["list_name"])

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
