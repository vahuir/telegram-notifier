# Telegram Notifier

Simple Python 3 application for running bash scripts and recieve notifications.

**You will need a Bot Token and your chat ID.**

For more information, you can read the Telegram's tutorial **From BotFather to 'Hello World'**:

[https://core.telegram.org/bots/tutorial](https://core.telegram.org/bots/tutorial)

# Usage

```
telegram-notifier command [cmd-arg1 ... cmd-argN]
```

Example (void process that runs for 2 minutes, and you will recieve a notification every 30 seconds):

```
telegram-notifier --ping 0.5 sleep 120
```

# Commandline options

```
usage: telegram-notifier [-h] [--process-name PROCESS_NAME] [--ping-time PING_TIME] [--bot-token BOT_TOKEN] [--file-bot-token FILE_BOT_TOKEN] [--chat-id CHAT_ID] [--file-chat-id FILE_CHAT_ID]

options:
  -h, --help            show this help message and exit
  --process-name PROCESS_NAME
                        Custom name for the process
  --ping-time PING_TIME
                        Every X minutes will send a message, verifying that the process is running. (0 disables the ping message)
  --bot-token BOT_TOKEN
                        Telegram BOT token
  --file-bot-token FILE_BOT_TOKEN
                        File where the Telegram BOT token is stored (default: ~/.telegram_bot_token)
  --chat-id CHAT_ID     Telegram chat id
  --file-chat-id FILE_CHAT_ID
                        File where the Telegram chat id is stored (default: ~/.telegram_chat_id)
```
