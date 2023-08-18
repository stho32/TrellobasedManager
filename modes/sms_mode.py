from datetime import datetime, time
from time import sleep
from library.sms_interface import send_sms
from library.trello_utils import check_task_exists, get_board_id, get_list_id, get_next_task, get_tasks, move_card, rename_task_if_about_time

def sms_mode(config):
    while True:  # Create an infinite loop
        send_sms_with_task(config)
        sleep(60)


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