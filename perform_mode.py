from datetime import datetime, timedelta
import random
import time
from library.chatgpt import send_prompt_to_gpt
from library.output_utils import print_and_speak
from library.task_utils import print_task, select_random_task
from library.trello_utils import get_all_lists, get_tasks
from library.sound_utils import play_mp3_async
from library.feedback import user_input_menu


def select_and_print_task(config, args, list_name):
    play_mp3_async("chinese-gong-daniel_simon.mp3")
    tasks = get_tasks(config, list_name)

    if not tasks:
        print_and_speak("No tasks found.")
        return False, None

    random_task = select_random_task(tasks)
    alternative_tasks = [task for task in tasks if task != random_task]
    random.shuffle(alternative_tasks)
    alternative_tasks = alternative_tasks[:2]  # Select two alternative tasks

    next_time = datetime.now() + timedelta(minutes=args.work_duration)
    print_task(random_task, next_time, alternative_tasks)

    task_in_english = send_prompt_to_gpt(
        "Consider this task: ```"
        + random_task["name"]
        + "``` Please translate it into english. If it already is english, just repeat the task."
    )

    print_and_speak("Your task is:" + task_in_english)
    intel = send_prompt_to_gpt(
        "Consider this task: ```"
        + task_in_english
        + "``` Which steps do you recommend to solve this task?"
    )
    print(intel)

    return True, random_task


def perform_work(config, args, list_name, rounds: int):
    all_lists = get_all_lists(config)
    round = rounds

    while True:
        task_found, current_task = select_and_print_task(config, args, list_name)
        if task_found:
            work_message = f"Working on the task for {args.work_duration} minutes."
            print_and_speak(work_message)
            time.sleep(args.work_duration * 60)  # Sleep for the specified work duration

            print_and_speak("Time for feedback.")
            play_mp3_async(
                "Rooster_Crowing-SoundBible.com-43612401.mp3"
            )  # Play the rooster crowing sound

            user_input_menu(current_task, all_lists, config)

            break_message = f"Time for a {args.break_duration} minute break."
            print_and_speak(break_message)

            next_task_time = datetime.now() + timedelta(minutes=args.break_duration)
            next_task_message = (
                f"Next task will be published at {next_task_time.strftime('%H:%M:%S')}."
            )
            print_and_speak(next_task_message)

            time.sleep(
                args.break_duration * 60
            )  # Sleep for the specified break duration

        else:
            retry_message = f"Retrying in {args.work_duration} minutes."
            print_and_speak(retry_message)
            time.sleep(args.work_duration * 60)  # Sleep for the specified work duration

        round -= 1
        if round == 0:
            print_and_speak("Finished all rounds.")
            break
