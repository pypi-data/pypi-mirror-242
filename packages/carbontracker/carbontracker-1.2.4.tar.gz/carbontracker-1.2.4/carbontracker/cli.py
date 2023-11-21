import argparse
import shlex
import subprocess
from carbontracker.tracker import CarbonTracker
import ast


def main():
    parser = argparse.ArgumentParser(description="CarbonTracker CLI")

    # Accept a list of arguments
    parser.add_argument("command", type=str, nargs='+',
                        help="Command and arguments to execute. E.g., 'python myscript.py arg1 arg2'")
    parser.add_argument("--log_dir", type=str, help="Log directory", default="./logs")
    parser.add_argument("--api_keys", type=str, help="API keys in a dictionary-like format, e.g., "
                                                     "'{\"electricitymaps\": \"YOUR_KEY\"}'", default=None)
    args = parser.parse_args()

    # Parse the API keys string into a dictionary
    api_keys = ast.literal_eval(args.api_keys) if args.api_keys else None

    tracker = CarbonTracker(epochs=1, log_dir=args.log_dir, epochs_before_pred=0, api_keys=api_keys)
    tracker.epoch_start()

    # Execute the provided command with its arguments
    try:
        subprocess.run(args.command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error executing command: {' '.join(map(shlex.quote, args.command))}")
        # Handle errors or exceptions if needed

    tracker.epoch_end()
    tracker.stop()


if __name__ == "__main__":
    main()
