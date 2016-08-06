# Telegram Pi Bot

## About

This is my personal [Telegram Bot](https://core.telegram.org/bots) to run on my [RaspberryPi 2](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) at home. It's supposed to be a proxy and an easy interface for all the home automation paraphernalia that we might end up getting in the future.

### Features

- Answers to only pre-configured chat rooms
- Webhooks configured via a JSON config file
 - Configures an endpoint to call for a given command
 - Works great with IFTTT Maker channel
- Basic multilingual support
 - `en` `pt-br`
- Runs on Python 3

## Setup

### Hardware requirements

- RaspberryPi
- Power cable
- MicroSD card
- Internet connection

### Installing things

This is a guide for the complete setup on ArchLinux, if you're just intested in running the script you can jump

*Base system setup*
- [Install archlinux](https://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2)
- [Add new user and change default passowrds](https://wiki.archlinux.org/index.php/users_and_groups)
- [Setup ssh](https://wiki.archlinux.org/index.php/Secure_Shell)
- [Setup sudo](https://wiki.archlinux.org/index.php/sudo)
- [Setup iptables](https://wiki.archlinux.org/index.php/iptables), [easier guide here](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-using-iptables-on-ubuntu-14-04) (make sure to open ports for ssh and supervisor)
- `systemctl enable iptables`
- [Configure static ip address](https://wiki.archlinux.org/index.php/systemd-networkd)

*Python setup*
- Install Python: `sudo pacman -S python`
- Install pip: `sudo pacman -S python-pip`

*Process management setup*
- `sudo pacman -S gcc`
- `sudo pacman -S python-setuptools`
- [Get circus for process management](http://circus.readthedocs.org/en/latest/)
- `sudo pip install circus`
- [Start circus on boot](http://circus.readthedocs.org/en/latest/for-ops/deployment/)

*Finally, bot setup*
- `sudo pip install telegram-pi-bot`
- Configure a `~/circus.ini` file
```
[circus]

[watcher:telegram-pi-bot]
cmd = telegram-pi-bot
numprocesses = 1

[env]
TELEGRAM_PI_BOT_CONFIG = /home/username/config.json
```
- Setup the [json config file](https://github.com/ruyadorno/telegram-pi-bot#config-file)

### Maintenance

- `sudo pacman -Syu` Updates the system

## Running the bot

### Config file

**Telegram Pi Bot** is configured through a `json` file, in which you can set your bot token and configure webhooks/commands to invoke from your bot.

Here is an example of what a `config.json` file looks like:

```json
{
    "bot_token": "<insert bot token>",
    "chat_ids": [
        "<insert chat id in which the bot should respond to>"
    ],
    "language": "<bot language>",
    "webhooks": [
        {
            "command_name": "dosomething",
            "url": "https://example.com/dosomething",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "data": { "value1": "%s" }
        }
    ]
}
```

### Locate config file

The config file will try to be loaded from:

- A location specified using the `TELEGRAM_PI_BOT_CONFIG` environment variable

_or_

- A `config.json` file placed in the same folder as the `main.py` script

### Using Circus

For improved process handling:

- `systemctl start circus`
- `systemctl stop circus`
- `systemctl reload circus`

Autostart on device boot:

- `systemctl enable circus`

### Script

Clone this repo, then `cd` into its folder.

To just simply run as a Python script, just make sure your `config.json` file is accessible as previously explained, then just run:

```sh
python telegram-pi-bot
```

## License

MIT © [Ruy Adorno](http://ruyadorno.com)

