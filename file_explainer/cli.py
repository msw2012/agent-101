"""
Command-line interface for the File Explainer Agent.
"""

import sys
import argparse
from pathlib import Path

from .agent import FileExplainerAgent


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Explain what a file does using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m file_explainer.cli auth.py
  python -m file_explainer.cli src/utils/helpers.js
  python -m file_explainer.cli --model claude-3-5-sonnet-20241022 script.py

Environment Variables:
  ANTHROPIC_API_KEY    Your Anthropic API key (required)
        """
    )

    parser.add_argument(
        "file",
        help="Path to the file to explain"
    )

    parser.add_argument(
        "--model",
        default="claude-3-5-sonnet-20241022",
        help="Claude model to use (default: claude-3-5-sonnet-20241022)"
    )

    parser.add_argument(
        "--api-key",
        help="Anthropic API key (overrides ANTHROPIC_API_KEY env var)"
    )

    args = parser.parse_args()

    try:
        # Initialize agent
        agent = FileExplainerAgent(api_key=args.api_key, model=args.model)

        # Get explanation
        print(f"Analyzing {args.file}...\n")
        explanation = agent.explain_file(args.file)

        # Print results
        print("=" * 80)
        print(f"File: {Path(args.file).resolve()}")
        print("=" * 80)
        print(explanation)
        print("=" * 80)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
