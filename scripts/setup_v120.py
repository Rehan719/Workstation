import os
import argparse
import getpass

def main():
    parser = argparse.ArgumentParser(description="Jules AI v120.0 Setup Wizard")
    parser.add_argument("--force", action="store_true", help="Overwrite existing .env file")
    args = parser.parse_args()

    env_path = ".env"
    if os.path.exists(env_path) and not args.force:
        print(f"{env_path} already exists. Use --force to overwrite.")
        return

    print("--- Jules AI v120.0 Apotheosis Setup Wizard ---")
    print("Please enter the following configuration details (press Enter to skip):")

    config = {}
    config["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key: ")
    config["ANTHROPIC_API_KEY"] = getpass.getpass("Anthropic API Key: ")
    config["QWEN_API_KEY"] = getpass.getpass("Qwen API Key (for v120.0 reasoning): ")
    config["LEGAL_API_KEY"] = getpass.getpass("CourtListener API Key: ")
    config["LINKEDIN_API_KEY"] = getpass.getpass("LinkedIn API Key: ")
    config["FIREBASE_CONFIG_JSON"] = input("Firebase Config JSON (minified): ")
    config["DATABASE_URL"] = input("Database URL (default: sqlite:///./jules_v120.db): ") or "sqlite:///./jules_v120.db"

    with open(env_path, "w") as f:
        for key, value in config.items():
            if value:
                f.write(f"{key}={value}\n")

    print(f"\nConfiguration saved to {env_path}")
    print("Setup complete. You are ready to launch the Apotheosis.")

if __name__ == "__main__":
    main()
