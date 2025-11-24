import os

# TOKEN
BOT_TOKEN = os.environ.get("7614551327:AAGHtL9QYpP4rbUdK9v_nlc1Pt5lLW7Bbuc")

# Telegram API settings
API_ID = int(os.environ.get("734531"))
API_HASH = os.environ.get("4ac3f42230e40a27cdcbaba52d754cb2")

# Video duration limit (minutes)
DURATION_LIMIT = int(os.environ.get("DURATION_LIMIT", 7))

# Command prefixes
COMMAND_PREFIXES = ["/", "!"]

# Sudo users
SUDO_USERS = list(map(int, os.environ.get("6895268368", "").split()))

# Force subscription channel (without @)
FORCE_CHANNEL = os.environ.get("xx_aa_i")
FORCE_GROUP = os.environ.get("zzmaa")  # optional

# Log group
LOG_GROUP_ID = int(os.environ.get("-1001840357767"))
