import requests
import json
import random

# Base URL for Trello API
BASE_URL = 'https://api.trello.com/1'


def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def get_board_id(config, board_name):
    url = f"{BASE_URL}/members/me/boards?key={config['API_KEY']}&token={config['TOKEN']}"
    response = requests.get(url)
    boards = response.json()

    for board in boards:
        if board['name'] == board_name:
            return board['id']

    return None


def get_list_id(config, board_id, list_name):
    url = f"{BASE_URL}/boards/{board_id}/lists?key={config['API_KEY']}&token={config['TOKEN']}"
    response = requests.get(url)
    lists = response.json()

    for list_obj in lists:
        if list_obj['name'] == list_name:
            return list_obj['id']

    return None


def get_tasks_in_list(config, list_id):
    url = f"{BASE_URL}/lists/{list_id}/cards?key={config['API_KEY']}&token={config['TOKEN']}"
    response = requests.get(url)
    return response.json()


def select_random_task(tasks):
    return random.choice(tasks)


def main():
    config = load_config()

    board_id = get_board_id(config, config['board_name'])

    if not board_id:
        print(f"No board found with the name '{config['board_name']}'.")
        return

    list_id = get_list_id(config, board_id, config['list_name'])

    if not list_id:
        print(f"No list found with the name '{config['list_name']}'.")
        return

    tasks = get_tasks_in_list(config, list_id)

    if not tasks:
        print(f"No tasks found in the list '{config['list_name']}'.")
        return

    random_task = select_random_task(tasks)

    print("\nYour task for today:")
    print("===================================")
    print(f"{random_task['name']}")
    print("===================================\n")


if __name__ == "__main__":
    main()
