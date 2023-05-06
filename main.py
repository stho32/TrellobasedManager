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
    next_time = datetime.now() + timedelta(minutes=args.work_duration)
    print_task(random_task, next_time)
    return True


def main():
    parser = argparse.ArgumentParser(description="Trello task selector.")
    parser.add_argument(
        "--work-duration",
        type=int,
        metavar="MINUTES",
        help="Specify the work duration in minutes for each task.",
    )
    parser.add_argument(
        "--break-duration",
        type=int,
        metavar="MINUTES",
        default=0,
        help="Specify the break duration in minutes after each task.",
    )

    args = parser.parse_args()

    config = load_config()

    if args.work_duration is not None:
        while True:
            task_found = select_and_print_task(config, args)
            if task_found:
                print(f"Working on the task for {args.work_duration} minutes.")
                time.sleep(
                    args.work_duration * 60
                )  # Sleep for the specified work duration

                print(f"Taking a {args.break_duration} minute break.")
                time.sleep(
                    args.break_duration * 60
                )  # Sleep for the specified break duration

            else:
                print(f"Retrying in {args.work_duration} minutes.")
                time.sleep(
                    args.work_duration * 60
                )  # Sleep for the specified work duration
    else:
        select_and_print_task(config, args)


if __name__ == "__main__":
    main()
