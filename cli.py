#!/usr/bin/env python3
"""CLI tool for iFlow search."""

import argparse
import sys

from iflow_client import search_web, format_search_result


def main():
    parser = argparse.ArgumentParser(
        description="Search the web using iFlow API",
        prog="iflow-search"
    )
    parser.add_argument(
        "query",
        help="Search query (use quotes for multi-word queries)"
    )
    parser.add_argument(
        "-r", "--raw",
        action="store_true",
        help="Output raw JSON response instead of formatted text"
    )

    args = parser.parse_args()

    try:
        result = search_web(args.query)
        if args.raw:
            import json
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_search_result(result))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
