import datetime
import random
import requests

from library.output_utils import print_and_speak


BASE_URL = "https://api.trello.com/1"


def get_board_id(config, board_name):
    url = (
        f"{BASE_URL}/members/me/boards?key={config['API_KEY']}&token={config['TOKEN']}"
    )
    response = requests.get(url)
    boards = response.json()

    for board in boards:
        if board["name"] == board_name:
            return board["id"]

    return None


def get_list_id(config, board_id, list_name):
    url = f"{BASE_URL}/boards/{board_id}/lists?key={config['API_KEY']}&token={config['TOKEN']}"
    response = requests.get(url)
    lists = response.json()

    for list_obj in lists:
        if list_obj["name"] == list_name:
            return list_obj["id"]

    return None


def get_random_task(config, list_name):
    tasks = get_tasks(config, list_name)
    if not tasks:
        print(f"No tasks found in the list '{list_name}'.")
        return None

    task = random.choice(tasks)
    return task

def get_next_task(config, list_name):
    """
    Get the next task from the top of a specified list.
    
    Args:
        config (dict): Configuration data including API keys.
        list_name (str): Name of the list from which to get the next task.
        
    Returns:
        (dict) The next task from the top of the list, or None if the list is empty.
    """
    tasks = get_tasks(config, list_name)
    if not tasks:
        print(f"No tasks found in the list '{list_name}'.")
        return None
    
    task = tasks[0]
    return task

def get_tasks(config, list_name):
    board_id = get_board_id(config, config["board_name"])

    if not board_id:
        print(f"No board found with the name '{config['board_name']}'.")
        return []

    list_id = get_list_id(config, board_id, list_name)

    if not list_id:
        print(f"No list found with the name '{list_name}'.")
        return []

    url = f"{BASE_URL}/lists/{list_id}/cards?key={config['API_KEY']}&token={config['TOKEN']}"
    response = requests.get(url)
    return response.json()


def delete_card(config, card_id):
    api_key = config["API_KEY"]
    api_token = config["TOKEN"]

    url = f"https://api.trello.com/1/cards/{card_id}"

    headers = {"Accept": "application/json"}

    query = {"key": api_key, "token": api_token}

    response = requests.request("DELETE", url, headers=headers, params=query)

    if response.status_code == 200:
        print("Task deleted successfully.")
    else:
        print("Failed to delete the task.")


def get_all_tasks(config, exclude_lists=None):
    board_id = get_board_id(config, config["board_name"])

    if not board_id:
        print(f"No board found with the name '{config['board_name']}'.")
        return []

    url = f"{BASE_URL}/boards/{board_id}/cards?key={config['API_KEY']}&token={config['TOKEN']}"
    response = requests.get(url)
    tasks = response.json()

    # Exclude tasks from specified lists
    if exclude_lists:
        tasks = exclude_tasks_from_lists(config, tasks, exclude_lists)

    return tasks


def exclude_tasks_from_lists(config, tasks, exclude_lists):
    """
    Exclude tasks from specified lists.
    """
    board_id = get_board_id(config, config["board_name"])

    if not board_id:
        print(f"No board found with the name '{config['board_name']}'.")
        return tasks

    # Get IDs of lists to exclude
    exclude_list_ids = []
    for list_name in exclude_lists:
        list_id = get_list_id(config, board_id, list_name)
        exclude_list_ids.append(list_id)

    # Exclude tasks from specified lists
    filtered_tasks = []
    for task in tasks:
        if task["idList"] not in exclude_list_ids:
            filtered_tasks.append(task)

    return filtered_tasks


def get_all_lists(config):
    board_id = get_board_id(config, config["board_name"])

    if not board_id:
        print(f"No board found with the name '{config['board_name']}'.")
        return []

    url = f"{BASE_URL}/boards/{board_id}/lists?key={config['API_KEY']}&token={config['TOKEN']}"
    response = requests.get(url)
    return response.json()


def move_card(config, card_id, target_list_id, pos=None):
    """
    Move a card to a specified list and optionally update its position within that list.

    Args:
        config (dict): Configuration data including API keys.
        card_id (str): ID of the card to be moved.
        target_list_id (str): ID of the target list.
        pos (int, optional): Position within the list. If None, card's position remains unchanged.

    Returns:
        None
    """
    api_key = config["API_KEY"]
    api_token = config["TOKEN"]

    url = f"https://api.trello.com/1/cards/{card_id}"

    headers = {"Accept": "application/json"}

    query = {
        "key": api_key,
        "token": api_token,
        "idList": target_list_id
    }
    
    if pos is not None:
        query["pos"] = pos

    response = requests.request("PUT", url, headers=headers, params=query)

    if response.status_code == 200:
        if pos is None:
            print("Task moved successfully.")
        else:
            print("Task moved and position updated successfully.")
    else:
        print("Failed to move the task.")



def check_task_exists(config, task_name):
    tasks = get_all_tasks(config)
    for task in tasks:
        if task["name"] == task_name:
            return True
    return False

def rename_task(config, card_id, new_name):
    api_key = config["API_KEY"]
    api_token = config["TOKEN"]

    url = f"{BASE_URL}/cards/{card_id}"

    headers = {"Accept": "application/json"}

    query = {"key": api_key, "token": api_token, "name": new_name}

    response = requests.request("PUT", url, headers=headers, params=query)

    if response.status_code == 200:
        print(f"Card name updated successfully to '{new_name}'.")
    else:
        print(f"Failed to update the card name.")

def get_task_by_name(config, task_name):
    tasks = get_all_tasks(config)
    for task in tasks:
        if task["name"] == task_name:
            return task
    return None

def rename_task_if_about_time(config, specified_time, old_name, new_name):
    # Get current time
    now = datetime.now().time()

    # Define "about time" as within 5 minutes of the specified time
    lower_bound = (datetime.combine(datetime.today(), specified_time) - datetime.timedelta(minutes=5)).time()
    upper_bound = (datetime.combine(datetime.today(), specified_time) + datetime.timedelta(minutes=5)).time()

    # Check if it is "about time"
    if time_within_range(lower_bound, upper_bound, now):
        # Check if the task exists with the old name
        if check_task_exists(config, old_name):
            task = get_task_by_name(config, old_name)
            if task['name'] == old_name:
                rename_task(config, task['id'], new_name)  # Update the task name
                print(f"Renamed task from {old_name} to {new_name}")

def time_within_range(start, end, now=None):
    now_time = now or datetime.now().time()

    if start <= end:
        return start <= now_time <= end
    else:  # Over midnight
        return start <= now_time or now_time <= end

def shuffle_tasks_in_list(config, list_name):
    """
    Shuffles the order of tasks in a specified list on Trello.

    Args:
        config (dict): Configuration data including API keys.
        list_name (str): Name of the list whose tasks are to be shuffled.

    Returns:
        None
    """
    # Get tasks from the specified list
    tasks = get_tasks(config, list_name)

    if not tasks:
        print(f"No tasks found in the list '{list_name}'.")
        return

    # Shuffle tasks locally
    random.shuffle(tasks)

    # Use the Trello position property to reorder tasks on the board.
    # Assuming we start at a base position and double it for each card.
    pos_val = 16384

    for task in tasks:
        update_card_pos(config, task["id"], pos_val)
        pos_val *= 2

    print(f"Tasks in the list '{list_name}' have been shuffled successfully.")


def update_card_pos(config, card_id, pos_val):
    """
    Updates the position (pos) of a card on Trello.

    Args:
        config (dict): Configuration data including API keys.
        card_id (str): ID of the card to be updated.
        pos_val (int): New position value for the card.

    Returns:
        None
    """
    api_key = config["API_KEY"]
    api_token = config["TOKEN"]

    url = f"{BASE_URL}/cards/{card_id}"

    headers = {"Accept": "application/json"}

    query = {
        "key": api_key,
        "token": api_token,
        "pos": pos_val
    }

    response = requests.put(url, headers=headers, params=query)

    if response.status_code != 200:
        print(f"Failed to update the position of card with ID {card_id}.")

def move_task_to_top(config, list_name, task_name):
    """
    Moves a specific task to the top of a specified list on Trello.

    Args:
        config (dict): Configuration data including API keys.
        list_name (str): Name of the list where the task resides.
        task_name (str): Name of the task to be moved to the top.

    Returns:
        None
    """
    tasks = get_tasks(config, list_name)

    if not tasks:
        print(f"No tasks found in the list '{list_name}'.")
        return

    # Find the task by name
    task_to_move = None
    for task in tasks:
        if task["name"] == task_name:
            task_to_move = task
            break

    if not task_to_move:
        print(f"No task found with the name '{task_name}' in the list '{list_name}'.")
        return

    # Get the position of the first task in the list
    top_task_pos = tasks[0]['pos']

    # Adjust the position value slightly lesser than the top task's position
    new_pos = top_task_pos - 1

    # Update the task's position to move it to the top
    update_card_pos(config, task_to_move["id"], new_pos)

    print(f"Moved '{task_name}' to the top of the list '{list_name}'.")

def reorder_tasks_by_sorted_list(config, list_name, sorted_tasks):
    """
    Reorders the tasks in a Trello list based on a provided sorted list of tasks.

    Args:
        config (dict): Configuration data including API keys.
        list_name (str): The name of the list to reorder tasks.
        sorted_tasks (list): A list of sorted tasks to dictate the new order.

    Returns:
        None
    """
    board_id = get_board_id(config, config["board_name"])
    list_id = get_list_id(config, board_id, list_name)

    base_pos_value = 65536

    # Set the position for each task in the sorted list
    for index, task in enumerate(sorted_tasks):
        new_pos = base_pos_value * (index + 1)  # Increase position value by the base value for each task
        move_card(config, task["id"], list_id, pos=new_pos)


