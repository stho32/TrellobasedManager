import json
import requests

from output_utils import print_and_speak


BASE_URL = "https://api.trello.com/1"


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


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


def get_tasks(config):
    board_id = get_board_id(config, config["board_name"])

    if not board_id:
        print(f"No board found with the name '{config['board_name']}'.")
        return []

    list_id = get_list_id(config, board_id, config["list_name"])

    if not list_id:
        print(f"No list found with the name '{config['list_name']}'.")
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
        print_and_speak("Task deleted successfully.")
    else:
        print_and_speak("Failed to delete the task.")
