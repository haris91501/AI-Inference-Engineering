"""CLI entry point for inference client."""

import argparse
from inference_client.config import load_config


def parse_args():
    parser = argparse.ArgumentParser(description="AI Inference Client CLI")
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to inference config JSON file (default: infer-config.json if present)",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=None,
        help="Inference API base URL",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model name to run inference against",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config)
    
    if args.base_url:
        config.base_url = args.base_url
    if args.model:
        config.model = args.model

    print(f"Inference Client initialized with base URL: {config.base_url}, model: {config.model}")


if __name__ == "__main__":
    main()
