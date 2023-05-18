import argparse
from performing_tasks import perform_work
from trello_utils import load_config


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

    args = parser.parse_args()

    config = load_config()

    # check if the perform flag is set
    if args.perform:
        # start the work process
        perform_work(config, args)
    else:
        print("The perform flag was not set, exiting program.")
        exit()


if __name__ == "__main__":
    main()
