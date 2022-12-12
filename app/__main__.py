import argparse
from app.main import main

def cli(args=None):
    parser = argparse.ArgumentParser(description='Run API and scheduler.')

    parser.add_argument('--no-api', dest='fastapi', action='store_false', help="Don't start the API.")
    parser.add_argument('--no-scheduler', dest='rocketry', action='store_false', help="Don't start the scheduler.")

    parser.set_defaults(fastapi=True, rocketry=True)

    args = parser.parse_args(args)

    main(
        fastapi=args.fastapi,
        rocketry=args.rocketry,
    )

if __name__ == "__main__":
    cli()