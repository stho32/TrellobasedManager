import argparse
import time
from datetime import datetime, timedelta
import pyttsx3
from task_utils import print_task, select_random_task
from trello_utils import load_config, get_tasks, get_board_id, get_list_id
from sound_utils import play_mp3_async


def print_and_speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def select_and_print_task(config, args):
    play_mp3_async("chinese-gong-daniel_simon.mp3")
    tasks = get_tasks(config)

    if not tasks:
        print_and_speak("No tasks found.")
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
        default=25,
        help="Specify the work duration in minutes for each task.",
    )
    parser.add_argument(
        "--break-duration",
        type=int,
        metavar="MINUTES",
        default=5,
        help="Specify the break duration in minutes after each task.",
    )

    args = parser.parse_args()

    config = load_config()

    if args.work_duration is not None:
        while True:
            task_found = select_and_print_task(config, args)
            if task_found:
                work_message = f"Working on the task for {args.work_duration} minutes."
                print_and_speak(work_message)
                time.sleep(
                    args.work_duration * 60
                )  # Sleep for the specified work duration

                break_message = f"Taking a {args.break_duration} minute break."
                print_and_speak(break_message)
                play_mp3_async(
                    "Rooster_Crowing-SoundBible.com-43612401.mp3"
                )  # Play the rooster crowing sound
                time.sleep(
                    args.break_duration * 60
                )  # Sleep for the specified break duration

            else:
                retry_message = f"Retrying in {args.work_duration} minutes."
                print_and_speak(retry_message)
                time.sleep(
                    args.work_duration * 60
                )  # Sleep for the specified work duration
    else:
        select_and_print_task(config, args)


if __name__ == "__main__":
    main()
