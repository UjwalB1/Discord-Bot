# Uji Bot

A Discord bot written in Python. It handles moderation, welcomes new members, answers questions with a magic 8-ball, and uses Google's Gemini API to summarize recent chat.

[Invite Uji to your server](https://discord.com/oauth2/authorize?client_id=1450929907638206565&permissions=8&integration_type=0&scope=applications.commands+bot) (asks for administrator so every command works). The bot is hosted for free and stays up as long as the server is renewed each week.

## Commands

Every command works as a slash command (`/kick`) or with the `uji ` prefix (`uji kick`).

| Command | What it does | Who can use it |
| --- | --- | --- |
| `summarize [channel]` | Summarizes the last 200 messages in a channel. Once every 10 minutes per server, and about 20 times a day on Gemini's free plan. | Anyone who can read that channel |
| `timeout <member> <amount> <s/m/h/d> [reason]` | Times out a member for up to 28 days | Timeout Members |
| `kick <member> [reason]` | Kicks a member and DMs them the reason | Kick Members |
| `ban <member> [reason]` | Bans a member and DMs them the reason | Ban Members |
| `set_welcome <channel>` | Sets where welcome messages are posted | Manage Server |
| `8ball <question>` | Answers a yes or no question | Anyone |
| `uji sync` | Registers slash commands with Discord | Bot owner |

Moderators can't act on members whose role is equal to or higher than their own. The bot's role also has to be above anyone it moderates.

## Setup

1. Install Python 3.10 or newer, then run `pip install -r requirements.txt`.
2. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications) and turn on the Server Members and Message Content intents.
3. Invite it to your server with the `bot` and `applications.commands` scopes.
4. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
5. Create a `.env` file in the project folder:

   ```
   DISCORD_TOKEN=your-discord-token
   GEMINI_KEY=your-gemini-key
   ```

6. Run `python main.py`, then type `uji sync` in your server once so the slash commands show up.

## Project layout

```
main.py          Starts the bot, loads every file in cogs/, handles command errors
cogs/
  general.py     Welcome messages and welcome channel settings
  moderation.py  Timeout, kick, ban
  summarizer.py  Gemini chat summaries
  gimmicks.py    Magic 8-ball
```

## Privacy

`summarize` sends message text and display names from the chosen channel to Google's Gemini API.
