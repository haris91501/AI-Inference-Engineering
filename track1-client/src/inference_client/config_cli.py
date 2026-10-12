import argparse
from inference_client.config import write_sample_config


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="infer-config",
        description="Inference client configuration utility",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Generate a sample configuration file",
    )
    args = parser.parse_args()
    if args.sample:
        write_sample_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
