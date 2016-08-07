# Telegram Pi Bot

## About

This is my personal [Telegram Bot](https://core.telegram.org/bots) to run on my [RaspberryPi](https://www.raspberrypi.org/products/pi-zero/) at home. It's supposed to be a proxy and an easy interface for all the home automation paraphernalia that we might end up getting in the future.

The bot can also be used in any system that has Python 3 support but the setup instructions provided are focused on getting it to work on the ARM architecture running on ArchLinux.

### Features

- Answers to only pre-configured chat rooms
- Webhooks configured via a JSON config file
 - Configures an endpoint to call for a given command
 - Works great with IFTTT Maker channel
- Basic multilingual support
 - `en` `pt-br`

## Setup

### Hardware requirements

- RaspberryPi
- Power cable
- MicroSD card
- Internet connection

### Installing things

This is a guide for the complete setup on ArchLinux, if you're just intested in running the script you can jump to [Process management setup](https://github.com/ruyadorno/telegram-pi-bot#process-management-setup).

_Remember to replace occurrences of **username** with your own user name._

#### Base system setup

A more complete step-by-step guide on how to set up ArchLinux on a RaspberryPi Zero is available here: https://gist.github.com/ruyadorno/08a04f5fcb37204767ce0942c9df8f91

- [Install archlinux](https://archlinuxarm.org/)
- [Add new user and change default passowrds](https://wiki.archlinux.org/index.php/users_and_groups)
- [Setup ssh](https://wiki.archlinux.org/index.php/Secure_Shell)
- [Setup sudo](https://wiki.archlinux.org/index.php/sudo)
- [Setup iptables](https://wiki.archlinux.org/index.php/iptables), [easier guide here](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-using-iptables-on-ubuntu-14-04) (make sure to open ports for ssh)
- `systemctl enable iptables`
- [Configure static ip address](https://wiki.archlinux.org/index.php/systemd-networkd)

#### Python setup
- Install Python: `sudo pacman -S python`
- Install pip: `sudo pacman -S python-pip`

#### Process management setup
- `sudo pacman -S gcc`
- `sudo pacman -S python-setuptools`
- [Get circus for process management](http://circus.readthedocs.org/en/latest/)
- `sudo pip install circus`

#### Bot setup
- Install the bot: `sudo pip install telegram-pi-bot`
- Setup the [json config file](https://github.com/ruyadorno/telegram-pi-bot#config-file)
- Test that the bot runs with the current config:
 - `telegram-pi-bot /home/username/config.json`
- CTRL+C to quit the process

#### Process management config
- Configure a `/home/username/circus.ini` file:
```
[circus]

[watcher:telegram-pi-bot]
cmd = telegram-pi-bot /home/username/config.json
numprocesses = 1
```
- Configure a `/etc/systemd/system/circus.service` file for autoload on boot:
```
[Unit]
Description=Circus process manager
After=syslog.target network.target nss-lookup.target

[Service]
Type=simple
ExecReload=/usr/bin/circusctl reload
ExecStart=/usr/bin/circusd /home/username/circus.ini
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```
- Reload **systemd**: `systemctl --system daemon-reload`
- Starts **circus** for the first time: `systemctl start circus`
- Enable **circus** to autostart on boot: `systemctl enable circus`
- More info on how to [Start circus on boot](http://circus.readthedocs.org/en/latest/for-ops/deployment/)

### Maintenance

- `sudo pacman -Syu` Updates the system

## Config file

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

The config file will try to be loaded in the following order:

- The first argument provided:
 - `telegram-pi-bot /home/username/config.json`
- A location specified using the `TELEGRAM_PI_BOT_CONFIG` environment variable:
 - `export TELEGRAM_PI_BOT_CONFIG=/home/username/config.json`
- A file named `config.json` placed inside the `telegram_pi_bot` folder

### Using Circus

For improved process handling:

- `systemctl start circus`
- `systemctl stop circus`
- `systemctl reload circus`

Autostart on device boot:

- `systemctl enable circus`

## License

MIT © [Ruy Adorno](http://ruyadorno.com)

