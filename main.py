"""Discord streaming status (selfbot).

Sets the purple "Streaming" status on your own Discord account.

Requires discord.py-self (NOT the regular discord.py) and Python 3.10+.
Using a user token with automation is against Discord's Terms of Service
and can get your account disabled. Use at your own risk.
"""

import json
import os
import sys
from pathlib import Path

import discord

CONFIG_PATH = Path(__file__).with_name("config.json")

DEFAULTS = {
    "name": "@toxiu.me",                    # text after "Streaming ..."
    "url": "https://twitch.tv/something",   # must be a twitch.tv or youtube.com link
    "status": "online",                     # online / idle / dnd / invisible
}


def load_config() -> dict:
    config = dict(DEFAULTS)
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open(encoding="utf-8") as f:
            config.update(json.load(f))

    # Environment variable wins over the file, so the token never has to be on disk.
    token = os.environ.get("DISCORD_TOKEN") or config.get("token", "")
    if not token or token == "paste ur token here":
        sys.exit(
            "No token. Set DISCORD_TOKEN or put it in config.json "
            "(copy config.example.json to config.json)."
        )
    config["token"] = token.strip().strip('"')

    if not config["url"].startswith(("https://twitch.tv/", "https://www.twitch.tv/",
                                     "https://youtube.com/", "https://www.youtube.com/")):
        print("Warning: Discord only shows the Streaming status for twitch.tv / youtube.com URLs.")

    return config


def main() -> None:
    config = load_config()

    activity = discord.Activity(
        type=discord.ActivityType.streaming,
        name=config["name"],
        url=config["url"],
    )

    try:
        status = discord.Status(config["status"])
    except ValueError:
        sys.exit(f"Unknown status {config['status']!r}, use online / idle / dnd / invisible.")

    # Passing the presence to the constructor makes the library send it on every
    # (re)connect, so the status survives gateway reconnects.
    client = discord.Client(activity=activity, status=status)

    @client.event
    async def on_ready():
        print(f"Logged in as {client.user} - streaming {config['name']!r} ({config['url']})")

    try:
        client.run(config["token"])
    except discord.LoginFailure:
        sys.exit("Login failed: the token is invalid or expired. Grab a fresh one and try again.")


if __name__ == "__main__":
    main()
