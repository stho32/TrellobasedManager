from datetime import datetime
from library.trello_utils import get_all_tasks, get_board_id, get_tasks, move_card, get_list_id, reorder_tasks_by_sorted_list, shuffle_tasks_in_list

def autocleanup_mode(config):
    move_tasks_of_the_day_to_todo_list(config)
    shuffle_tasks_in_list(config, config["list_name"])
    sort_tasks_by_priority(config, config["list_name"])

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

def extract_priority(task_name):
    """
    Extracts the priority number from the task name.

    Args:
        task_name (str): The name of the task.

    Returns:
        int: The extracted priority number or 0 if not found.
    """
    tags = extract_tags(task_name)

    # Search for the "prio:" tag
    for tag in tags:
        if tag.startswith('prio:'):
            try:
                return int(tag[5:])  # Extract the integer value after "prio:"
            except ValueError:  # In case the conversion to integer fails
                return 0

    return 0

def sort_tasks_by_priority(config, list_name):
    """
    Sorts the tasks in the specified list by their priority number in descending order.

    Args:
        config (dict): Configuration data including API keys.
        list_name (str): The name of the list to sort tasks.

    Returns:
        None
    """
    tasks = get_tasks(config, list_name)
    sorted_tasks = sorted(tasks, key=lambda task: extract_priority(task["name"]), reverse=True)
    
    # Reorder the tasks based on their sorted order
    reorder_tasks_by_sorted_list(config, list_name, sorted_tasks)
