import argparse
from performing_tasks import perform_work
from trello_utils import load_config


def cleanup(config, args):
    all_tasks = get_all_tasks(config)

    if not all_tasks:
        print("No tasks found.")
        return
    # Further processing of tasks...


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
    parser.add_argument(
        "--perform",
        action="store_true",
        help="Specify this flag to start the work process.",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Specify this flag to start the cleanup process.",
    )

    args = parser.parse_args()

    config = load_config()

    # check if the perform flag is set
    if args.perform:
        # start the work process
        perform_work(config, args)
    elif args.cleanup:
        # start the cleanup process
        cleanup(config, args)
    else:
        print("Neither the perform nor the cleanup flag was set, exiting program.")
        exit()


if __name__ == "__main__":
    main()
