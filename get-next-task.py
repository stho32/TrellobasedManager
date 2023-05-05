# Replace these with your Trello API key and token
import requests

# Replace these with your Trello API key and token
API_KEY = ''
TOKEN = ''

# Base URL for Trello API
BASE_URL = 'https://api.trello.com/1'


def get_board_id(board_name):
    url = f"{BASE_URL}/members/me/boards?key={API_KEY}&token={TOKEN}"
    response = requests.get(url)
    boards = response.json()

    for board in boards:
        if board['name'] == board_name:
            return board['id']

    return None


def get_list_id(board_id, list_name):
    url = f"{BASE_URL}/boards/{board_id}/lists?key={API_KEY}&token={TOKEN}"
    response = requests.get(url)
    lists = response.json()

    for list_obj in lists:
        if list_obj['name'] == list_name:
            return list_obj['id']

    return None


def get_tasks_in_list(list_id):
    url = f"{BASE_URL}/lists/{list_id}/cards?key={API_KEY}&token={TOKEN}"
    response = requests.get(url)
    return response.json()


def main():
    board_name = input("Enter the name of the board: ")
    board_id = get_board_id(board_name)

    if not board_id:
        print(f"No board found with the name '{board_name}'.")
        return

    list_name = input("Enter the name of the list: ")
    list_id = get_list_id(board_id, list_name)

    if not list_id:
        print(f"No list found with the name '{list_name}'.")
        return

    tasks = get_tasks_in_list(list_id)

    print(f"Tasks in list '{list_name}':")
    for task in tasks:
        print(f"- {task['name']}")

if __name__ == "__main__":
    main()
