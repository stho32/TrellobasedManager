import argparse
from modes.cleanup_mode import cleanup
from modes.perform_mode import perform_work
from library.configuration import load_config
from modes.simple_mode import simple_mode
from modes.sms_mode import sms_mode
from modes.autocleanup_mode import autocleanup_mode

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
    parser.add_argument(
        "--list-name",
        type=str,
        help="Specify the name of the list to perform tasks on, only used with --perform flag.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=999,
        help="Specify the number of rounds to perform tasks, only used with --perform flag.",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Specify this flag to start the program in simple mode.",
    )
    parser.add_argument(
        "--sms",
        action="store_true",
        help="Specify this flag to send an SMS.",
    )
    parser.add_argument(
        "--autocleanup",
        action="store_true",
        help="Specify this flag to start the auto cleanup process.",
    )

    args = parser.parse_args()

    config = load_config()

    list_name = args.list_name
    if args.list_name is None:
        list_name = config["list_name"]

    if args.perform:
        perform_work(config, args, list_name, args.rounds)
    elif args.cleanup:
        cleanup(config, args)
    elif args.simple:
        simple_mode(config, list_name)
    elif args.sms:
        sms_mode(config)
    elif args.autocleanup:
        autocleanup_mode(config)
    else:
        print(
            "Neither the perform, cleanup, simple, sms, nor autocleanup flag was set, exiting program."
        )
        exit()

if __name__ == "__main__":
    main()
