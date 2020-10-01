# discord_cakebot
[![Documentation Status](https://readthedocs.org/projects/discord-cakebot/badge/?version=latest)](http://discord-cakebot.readthedocs.io/en/latest/?badge=latest)

General-purpose bot for discord.

## Requirements
Packages below are also listed in `requirements.txt`.
* Python >= 3.5
* [discordpy](https://github.com/Rapptz/discord.py)
* [PyNaCl](https://github.com/pyca/pynacl)
* [aiohttp](https://github.com/aio-libs/aiohttp)
* [requests](https://github.com/requests/requests)
* [pytest](https://github.com/pytest-dev/pytest)


## Setup
Clone the repo and `cd` into it:

	git clone https://github.com/leagueofcake/discord_cakebot.git && cd discord_cakebot

Install requirements via `pip`: 

	pip install -r requirements.txt

Rename `sample_config.py` to `cakebot_config.py` and update the values (mainly `TOKEN` (Discord API token) and `OWNER_ID`):

	mv sample_config.py cakebot_config.py

Run `run_bot.sh` or run the bot module directly with `python`:

	sh scripts/run_bot.sh
    # OR
    python -m bot
    
## Functionality
* **Music queuing (for music bots)**
    * Queueing songs from a song database
    * Queueing all songs from an album
    * Setting custom prefix for queueing songs (e.g. !play, ~play, !lm play)
* **Moderation**
    * Message logging (edits/deletions)
    * Purging messages (either by user or indiscriminately)
* **Shortcuts**
    * Deleting previous message
    * Generating Google search links within Discord
    * Redirecting message to another channel (post to another channel from your current channel)
* **Miscellaneous**
    * Sending pictures of cats in timed intervals :3
    * Trolling URLs (replace characters with similar looking ones)

Visit the [docs](https://discord-cakebot.readthedocs.io/en/latest/?) for a full command list.
