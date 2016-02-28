# Telegram Pi Bot

## About

This is my personal [Telegram Bot](https://core.telegram.org/bots) to run on my [RaspberryPi 2](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) at home. It's supposed to be a proxy and an easy interface for all the home automation paraphernalia that we might end up getting in the future.

## Setup

### Hardware requirements

- RaspberryPi 2
- Ethernet cable
- Power cable
- MicroSD card

### Installing things

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
- `sudo pip install circus-web`
- [Start circus on boot](http://circus.readthedocs.org/en/latest/for-ops/deployment/)

### Maintenance

- `sudo pacman -Syu` Updates the system

## Running the bot

*Config env variables*

- `BOT_TOKEN` Unique token from Telegram to use your bot
- `LANG` Language the bot should use [en|pt-br], defaults to `en`

### Using Circus

- `systemctl start circus`
- `systemctl stop circus`
- `systemctl reload circus`

### Alternative

Just export the `BOT_TOKEN` as a environment variable and launch the bot:

```sh
python main.py
```

## License

MIT © [Ruy Adorno](http://ruyadorno.com)

