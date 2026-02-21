#!/usr/bin/env python3
import sys
import os
import traceback

print(f"Python version: {sys.version}")
print(f"Current working dir: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    import config.settings
    print("config.settings imported")
    from config.settings import settings
    print(f"BOT_TOKEN: {repr(settings.BOT_TOKEN)}")
    print(f"ADMIN_CHAT_ID: {repr(settings.ADMIN_CHAT_ID)}")
    print(f"DATABASE_URL: {repr(settings.DATABASE_URL)}")
except Exception as e:
    print(f"Error importing config.settings: {type(e).__name__}: {e}")
    print(traceback.format_exc())

print("\n---\n")

try:
    import bot.main
    print("bot.main imported")
    from bot.main import bot
    print("Bot object:", repr(bot))
except Exception as e:
    print(f"Error importing bot.main: {type(e).__name__}: {e}")
    print(traceback.format_exc())
