import asyncio
import argparse
import json

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", required=True)
    args = parser.parse_args()
    print(f"MULTI-SIG COUNCIL ALERT: {args.message}")

if __name__ == "__main__":
    asyncio.run(main())
