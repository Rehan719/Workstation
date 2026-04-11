import argparse
import sys
import logging
import asyncio
from core.orchestration.workflow_orchestrator import MJMWorkflowOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mjm-cli")

async def run_command(args):
    orchestrator = MJMWorkflowOrchestrator()
    try:
        if args.command == "mushahida":
            chk_id = await orchestrator.run_mushahida(args.domain, args.queries, args.user)
            print(f"Mushahida completed. Checkpoint: {chk_id}")
        elif args.command == "jaiza":
            chk_id = await orchestrator.run_jaiza(args.checkpoint, args.user)
            print(f"Jaiza completed. Checkpoint: {chk_id}")
        elif args.command == "muaina":
            chk_id = await orchestrator.run_muaina(args.checkpoint, args.option, args.user)
            print(f"Muaina completed. Checkpoint: {chk_id}")
        else:
            print("Unknown command")
    except Exception as e:
        logger.error(f"Error executing {args.command}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="MJM Intelligence Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Mushahida
    mush_parser = subparsers.add_parser("mushahida", help="Run Observation phase")
    mush_parser.add_argument("--domain", default="patient_safety", help="Domain ID")
    mush_parser.add_argument("--queries", nargs="+", required=True, help="Search queries")
    mush_parser.add_argument("--user", default="default_user", help="User ID")

    # Jaiza
    jaiza_parser = subparsers.add_parser("jaiza", help="Run Evaluation phase")
    jaiza_parser.add_argument("--checkpoint", required=True, help="Mushahida checkpoint ID")
    jaiza_parser.add_argument("--user", default="default_user", help="User ID")

    # Muaina
    muaina_parser = subparsers.add_parser("muaina", help="Run Inspection phase")
    muaina_parser.add_argument("--checkpoint", required=True, help="Jaiza checkpoint ID")
    muaina_parser.add_argument("--option", required=True, help="Selected strategic option ID")
    muaina_parser.add_argument("--user", default="default_user", help="User ID")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    asyncio.run(run_command(args))

if __name__ == "__main__":
    main()
