from setuptools import setup

setup(
    version="1.0.0",
    name="telegram-notifier",
    description="Telegram Notifier executes bash commands and monitors them.",
    author="Vicent Ahuir",
    entry_points={"console_scripts": ["telegram-notifier = telegram_notifier:app"]},
    install_requires=["python-telegram-bot>=21.0.1"],
    python_requires=">=3.8.0",
)

