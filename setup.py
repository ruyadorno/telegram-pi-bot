from distutils.core import setup

setup(
    name = 'telegram-pi-bot',
    packages = [
        'telegram_pi_bot',
        'telegram_pi_bot.config',
        'telegram_pi_bot.msgs',
        'telegram_pi_bot.requests'
    ],
    version = '0.1.8',
    description = 'A python-telegram-bot setup to run on Raspberry pi',
    author = 'Ruy Adorno',
    author_email = 'ruyadorno@hotmail.com',
    url = 'https://github.com/ruyadorno/telegram-pi-bot',
    download_url = 'https://github.com/ruyadorno/telegram-pi-bot/tarball/0.1.8',
    keywords = ['telegram', 'raspberrypi', 'bot', 'python-telegram-bot'],
    install_requires=['python-telegram-bot>=5,<6'],
    classifiers = [],
    entry_points = {
        'console_scripts': [
            'telegram-pi-bot = telegram_pi_bot.command_line:main'
        ]
    }
)

