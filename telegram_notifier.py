#!/bin/python3


"""
Script for receiving messages in Telegram about the execution of a process.

version: 1.0
author: Vicent Ahuir Esteve (viahes@eui.upv.es)
"""

import io
import os
import sys
import time
import argparse
import asyncio
import platform

from typing import Optional
from datetime import datetime

import telegram


def get_bot_token(bot_token_file: str) -> Optional[str]:
    path = os.path.expanduser(bot_token_file)

    if os.path.exists(path):
        token_id = open(path).readlines()[0].strip()

        return token_id
    
    return None


def get_chat_id(chat_id_file: str) -> Optional[int]:
    path = os.path.expanduser(chat_id_file)

    if os.path.exists(path):
        chat_id = int(open(path).readlines()[0].strip())

        return chat_id
    

async def send_message(bot: telegram.Bot, chat_id:int, text: str) -> None:
    now = datetime.now().strftime("%b %d %Y %H:%M:%S")
    
    async with bot:
        await bot.send_message(
            chat_id=chat_id,
            text=f"_{now}\ \- *{platform.node()}*_\n{text}",
            parse_mode='MarkdownV2'
        )


async def ping_message(
    process_name, ping_time, bot, chat_id, flag
):
    remaning = ping_time

    while ping_time > 0: 
        await asyncio.sleep(1)

        if not flag[0]:
            break

        remaning -= 1

        if remaning == 0:
            await send_message(
                bot, chat_id, f"`{process_name}`\n\nStill running… 🦾"
            )
            remaning = ping_time


async def read_stream(stream, cb, flag):  
    while True:
        line = await stream.readline()
        if line:
            cb(line.decode("utf-8"))
        else:
            break

    flag[0] = False


async def stream_subprocess(cmd, process_name, bot, chat_id, ping_time):  
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    flag = [True]

    stdout_cb = lambda x: print(x, file=sys.stdout, end="")
    stderr_cb = lambda x: print(x, file=sys.stderr, end="")

    await asyncio.gather(
        read_stream(process.stdout, stdout_cb, flag),
        read_stream(process.stderr, stderr_cb, flag),
        ping_message(process_name, ping_time, bot, chat_id, flag)
    )

    return await process.wait()


async def main(cmd, process_name, bot_token, chat_id, ping_time):
    process_name = " ".join(cmd)

    bot = telegram.Bot(token=bot_token)

    await send_message(bot, chat_id, f"`{process_name}`\n\nStarting process\! 🤖")
    returncode = await stream_subprocess(cmd, process_name, bot, chat_id, ping_time)

    if returncode == 0:
        message = f"`{process_name}`\n\nProcess finished correctly\! 😁\n\n\n"

    else:
        message = f"`{process_name}`\n\nERROR\! 😰"

    await send_message(bot, chat_id, message)
    
    return returncode


def app():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--process-name", help="Custom name for the process"
    )
    parser.add_argument(
        "--ping-time", help="Every X minutes will send a message, verifying that the process is running. (0 disables the ping message)", default=10, type=float
    )
    parser.add_argument("--bot-token", help="Telegram BOT token")
    parser.add_argument("--file-bot-token", help="File where the Telegram BOT token is stored (default: ~/.telegram_bot_token)", default="~/.telegram_bot_token")
    parser.add_argument("--chat-id", help="Telegram chat id", type=int)
    parser.add_argument("--file-chat-id", help="File where the Telegram chat id is stored (default: ~/.telegram_chat_id)", default="~/.telegram_chat_id")

    args, cmd = parser.parse_known_args()

    bot_token = args.bot_token
    if bot_token is None:
        bot_token = get_bot_token(args.file_bot_token)

        if bot_token is None:
            raise ValueError("Bot token not found! Should be assinged by command or within the file")

    chat_id = args.chat_id
    if chat_id is None:
        chat_id = get_chat_id(args.file_chat_id)

        if chat_id is None:
            raise ValueError("Chat id not found! Should be assinged by command or within the file")

    # Time in seconds to send a message for
    # verifying that the process is sill running.
    ping_time = args.ping_time * 60

    process_name = args.process_name

    if process_name is None:
        process_name = " ".join(cmd)

    try:
        asyncio.run(main(cmd, process_name, bot_token, chat_id, ping_time))

    except asyncio.exceptions.CancelledError:
        bot = telegram.Bot(token=bot_token)
        asyncio.run(send_message(bot, chat_id, f"`{process_name}`\n\nCancelled\! 😵"))

if __name__ == "__main__":
    app()

