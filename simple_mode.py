from library.feedback import user_input_menu
from library.trello_utils import *
import random


def simple_mode(config, list_name):
    print("Starting simple mode.")
    update_task_positions_or_delete(config, list_name)


def update_task_positions_or_delete(config, list_name):
    all_lists = get_all_lists(config)

    if not all_lists:
        print("No lists found.")
        return

    while True:
        all_tasks = get_tasks(config, list_name)

        if not all_tasks:
            print("No tasks found.")
            return

        print(f"Remaining tasks: {len(all_tasks) - 1}")

        task = random.choice(all_tasks)
        should_continue = user_input_menu(task, all_lists, config)

        if not should_continue:
            break
