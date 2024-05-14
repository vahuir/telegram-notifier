from setuptools import setup, find_packages

setup(
    version="1.0.5",
    name="telegram-notifier",
    description="Telegram Notifier executes bash commands and monitors them.",
    author="Vicent Ahuir",
    packages=find_packages(),
    entry_points={"console_scripts": ["telegram-notifier = telegram_notifier.cli:app"]},
    install_requires=["python-telegram-bot>=21.0.1"],
    python_requires=">=3.8.0",
)

