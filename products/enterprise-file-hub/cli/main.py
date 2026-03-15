import argparse
import sys
from agentic_core.tools.file_operations import FileOperations

def main():
    parser = argparse.ArgumentParser(description="Workstation Enterprise File Hub CLI (wfh)")
    subparsers = parser.add_subparsers(dest="command")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload a file to the Sovereign Hub")
    upload_parser.add_argument("--file", required=True, help="Path to the file")
    upload_parser.add_argument("--classify", default="auto", help="File classification")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a configuration file")
    gen_parser.add_argument("--type", required=True, choices=["reactor", "charter"], help="Type of file to generate")
    gen_parser.add_argument("--name", required=True, help="Name of the entity")

    args = parser.parse_args()
    file_ops = FileOperations()

    if args.command == "upload":
        print(f"Uploading {args.file}...")
        result = file_ops.process_file_upload(args.file, {"classification": args.classify})
        print(f"Success: File ingested. Hash: {result['hash'][:16]}")

    elif args.command == "generate":
        if args.type == "reactor":
            content = file_ops.generate_reactor_config(args.name, {})
            print(f"Generated Reactor Config:\n{content}")
        else:
            print("Charter generation not yet implemented.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
