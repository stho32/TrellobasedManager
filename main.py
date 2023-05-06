import argparse
import time
from datetime import datetime, timedelta
from task_utils import print_task, select_random_task
from trello_utils import load_config, get_tasks, get_board_id, get_list_id
from sound_utils import play_mp3_async


def select_and_print_task(config):
    play_mp3_async("chinese-gong-daniel_simon.mp3")
    tasks = get_tasks(config)

    if not tasks:
        print("No tasks found.")
        return False

    random_task = select_random_task(tasks)
    next_time = datetime.now() + timedelta(hours=1)
    print_task(random_task, next_time)
    return True


def main():
    parser = argparse.ArgumentParser(description="Trello task selector.")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Enable loop mode to select tasks every hour.",
    )

    args = parser.parse_args()

    config = load_config()

    if args.loop:
        while True:
            task_found = select_and_print_task(config)
            if not task_found:
                print("Retrying in 1 hour.")
            time.sleep(3600)  # Sleep for 1 hour
    else:
        select_and_print_task(config)


if __name__ == "__main__":
    main()
