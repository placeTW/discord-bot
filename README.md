# PlaceTW Discord Bot

A bot developed by Taiwan's r/place community for various discord functions

To get support on this bot, visit the [bot-tech-support](https://discord.com/channels/959467908315111444/1137057312268374199) channel in our server https://discord.gg/8xSQKCHSnT

# Getting started

To get started on developing for this bot, you'll need the following:
- [Python](https://www.python.org/)
- A code editor

Start by cloning this project on your computer

## Setting up a virtual environment

This project uses Poetry to manage packages. Follow the instructions [here](https://python-poetry.org/docs/#installation) to get started with poetry.

Once you have poetry set up, run `poetry shell` to start the poetry virtual environment.

To install the packages required for this project, run `poetry install`. 


## Running the bot

To run the bot, run `python main.py`.

You'll need the following environment variables in a `.env` file for development:
```
DISCORD_TOKEN_DEV=
GITHUB_TOKEN=
YOUTUBE_API_KEY=
MODERATE_CONTENT_API_KEY=

PLACETW_SERVER_ID=
LOG_CHANNEL=

SUPABASE_URL=
SUPABASE_SECRET_KEY=
```

## Current Functionalities

### For Website

* `/ui-fetch`: Fetch placeTW entries by UI
* `/fetch <entry> <lang>`: Fetch placeTW entries by command line
* `/edit-entry <entry> <lang> <field>`: Edit placeTW entries and get approved/rejected in `#translation-submissions` channel

### For Fun

* `/hgs`: The most important question
* `/101`: Build 101 with random height by emojis

## Planned Functionalities

* `/track <lang>`: Track the translation progress of a language
* `/coord-list`: Show a list of all canvas our/ally coordinates
* `/coord <name>`: Show the canvas coordinates of one entry
* `/edit-coord <name> <x> <y>`: Update the canvas coordinates for one entry
* `/update-plan <announcement>`: Update a plan and post English text and translated Mandarin in some channels

## Future Functionalities
no

## Non-code-related steps
no

## Deployment & Testing

* Main bot: Runs on main branch, should be stable and not used for developing new features
* Dev bot: Runs on non-main branches, should test stuff with it
