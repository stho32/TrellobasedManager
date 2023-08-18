from library.feedback import user_input_menu
from library.trello_utils import (
    get_all_lists,
    get_all_tasks,
    get_tasks,
)
import random


def cleanup(config, args):
    print("Starting cleanup.")
    print("First part: Execution of planning session.")
    execute_planning_session(config)
    print("Second part: Update task positions or delete tasks.")
    update_task_positions_or_delete(config)

def execute_planning_session(config):
    planning_tasks = get_tasks(config, config["planning_activities_list_name"])
    
    for task in planning_tasks:
        print(task["name"])
        input("Press enter for the next task.")

def update_task_positions_or_delete(config):
    all_tasks = get_all_tasks(config, exclude_lists=[config["planning_activities_list_name"]])

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