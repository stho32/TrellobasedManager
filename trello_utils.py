import json
import random
import requests

from output_utils import print_and_speak


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


def move_card(config, card_id, target_list_id):
    api_key = config["API_KEY"]
    api_token = config["TOKEN"]

    url = f"https://api.trello.com/1/cards/{card_id}"

    headers = {"Accept": "application/json"}

    query = {"key": api_key, "token": api_token, "idList": target_list_id}

    response = requests.request("PUT", url, headers=headers, params=query)

    if response.status_code == 200:
        print("Task moved successfully.")
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
