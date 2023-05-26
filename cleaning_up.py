from feedback import user_input_menu
from trello_utils import (
    get_all_lists,
    get_all_tasks,
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
        should_continue = user_input_menu(task, all_lists, config)
        if not should_continue:
            break
