import argparse
import time
from datetime import datetime, timedelta
from task_utils import print_task, select_random_task
from trello_utils import load_config, get_tasks, get_board_id, get_list_id
from sound_utils import play_mp3_async


def select_and_print_task(config, args):
    play_mp3_async("chinese-gong-daniel_simon.mp3")
    tasks = get_tasks(config)

    if not tasks:
        print("No tasks found.")
        return False

    random_task = select_random_task(tasks)
    next_time = datetime.now() + timedelta(minutes=args.loop)
    print_task(random_task, next_time)
    return True


def main():
    parser = argparse.ArgumentParser(description="Trello task selector.")
    parser.add_argument(
        "--loop",
        type=int,
        metavar="MINUTES",
        help="Enable loop mode to select tasks every specified number of minutes.",
    )

    args = parser.parse_args()

    config = load_config()

    if args.loop is not None:
        while True:
            task_found = select_and_print_task(config, args)
            if not task_found:
                print(f"Retrying in {args.loop} minutes.")
            time.sleep(args.loop * 60)  # Sleep for the specified number of minutes
    else:
        select_and_print_task(config, args)


if __name__ == "__main__":
    main()
