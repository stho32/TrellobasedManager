from feedback import user_input_menu
from trello_utils import get_all_tasks, get_all_lists
import random


def simple_mode(config, args):
    print("Starting simple mode.")
    update_task_positions_or_delete(config)


def update_task_positions_or_delete(config):
    all_lists = get_all_lists(config)

    if not all_lists:
        print("No lists found.")
        return

    while True:
        all_tasks = get_all_tasks(
            config, exclude_lists=[config["planning_activities_list_name"]]
        )

        if not all_tasks:
            print("No tasks found.")
            return

        task = random.choice(all_tasks)
        should_continue = user_input_menu(task, all_lists, config)
        if not should_continue:
            break
