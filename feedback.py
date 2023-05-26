from trello_utils import delete_card, move_card


def user_input_menu(task, all_lists, config):
    print(f"\nTask: {task['name']}")

    for i, list_obj in enumerate(all_lists, start=1):
        print(f"{i}. {list_obj['name']}")

    print("d. Delete task")
    print("Press Enter to stop.\n")

    user_input = input("Choose an option: ")

    if user_input == "d":
        delete_card(config, task["id"])
        return True
    elif user_input.isdigit():
        list_index = int(user_input) - 1
        if 0 <= list_index < len(all_lists):
            move_card(config, task["id"], all_lists[list_index]["id"])
    elif user_input == "":
        return False
    else:
        print("Invalid option. Skipping this task.")

    return True
