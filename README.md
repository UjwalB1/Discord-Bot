## Uji, Discord-Bot
Uji is a simple multi-purpose Discord bot built with Discord.py, which is a API wrapper for Discord, and incorporates Google Gemini API for one of its features. In general a fun, bot with a mixture of moderation, general discord features like welcoming new members, as well as a unique summarization feature.

# Core features:
- Summarize (/summarize, or uji summarize): A command that can be used every 10 minutes within a Discord server, that fetches the last 200 messages from the message history of any target channel and summarizes in an unserious and potential snarky manner while still covering most details, using AI to provide the summary after fetching the messages and providing it to Gemini. Since it uses Gemini, it is rate limited to 20 uses per day (free plan)

- 8ball (uji 8ball {insert question} ): A simple fun gimmick command which responds with a yes or no answer in different ways selecting a different response out of the prewritten choices at random. In rare cases the bot may answer in a wild way instead of a providing a yes or no answer.

- Welcome System: Uses a JSON file to store server specific data, ensuring Uji remembers the set welcome channel even after a potential server shut down. If a dedicated channel is setup, Uji will welcome new members upon them joining in the target channel, otherwise welcomes in another channel that it has permission to do so in.
(uji sw {channel ping} ) to set the welcome channel.

- Moderation: Is capable of the simple expected moderation actions such as temporary muting/timing out, kicking, and banning members.
(uji kick, uji ban, can be used followed by pinging the user targeted.
(uji tm {duration} {duration type} for timeouts, for example, uji tm @user 45 s (s, h, d, representing seconds, hours, days, respectively.)


NOTE: May have to adjust the role permissions, and the hierarchy within discord servers to make sure all commands work. For example, only those with permissions can use moderation commands, and the bot itself needs permission to do certain actions.

# Installation and Requirement extra:
This project uses two API keys, a bot token from Discord, as well as an API key from Gemini which are stored in private .env files
Dependencies can be installed from the requirements.txt file, pip install -r requirements.txt

The bot is hosted for free, and should be up as long as I renew my server every week.

Uji bot can be invited via this link, which will ask you to provide administrator permissions so all commands can work smoothly:

[bot invite link](https://discord.com/oauth2/authorize?client_id=1450929907638206565&permissions=8&integration_type=0&scope=applications.commands+bot)
