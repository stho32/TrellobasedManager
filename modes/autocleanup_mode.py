from datetime import datetime
from library.trello_utils import get_all_tasks, get_board_id, move_card, get_list_id, shuffle_tasks_in_list

def autocleanup_mode(config):
    move_tasks_of_the_day_to_todo_list(config)
    shuffle_tasks_in_list(config, config["list_name"])

def move_tasks_of_the_day_to_todo_list(config):
    # Get the current weekday
    current_weekday = datetime.now().strftime('%A').lower()

    # Get all tasks, excluding the planning activities list
    all_tasks = get_all_tasks(config, exclude_lists=[config["planning_activities_list_name"]])

    # ID for the "Option for Today" list
    board_id = get_board_id(config, config["board_name"])
    today_list_id = get_list_id(config, board_id, config["list_name"])

    # Process each task
    for task in all_tasks:
        tags = extract_tags(task["name"])

        # Check for "daily" tag or the current weekday
        if "daily" in tags or current_weekday in tags:
            move_card(config, task["id"], today_list_id)

def extract_tags(task_name):
    start_idx = task_name.find('[')
    end_idx = task_name.find(']')

    if start_idx != -1 and end_idx != -1:
        tags_str = task_name[start_idx + 1:end_idx]
        return [tag.strip().lower() for tag in tags_str.split(',')]
    else:
        return []
