#!/usr/bin/env python

import logging
import config
import msgs
from requests import post_json
from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

# Gather initial data to start
logger = logging.getLogger(__name__)
msg = msgs.start(config.get('language'))
chats = config.get('chat_ids')


def simple_msg(bot, update, message):
    if (str(update.message.chat_id) in chats):
        bot.sendMessage(chat_id=update.message.chat_id, text=message)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=msg('forbidden'))


# Static methods
def start(bot, update):
    simple_msg(bot, update, msg('welcome'))


def help(bot, update):
    simple_msg(bot, update, msg('help') + get_webhook_names())


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def get_webhook_names():
    names = '\n'
    for webhook in config.get('webhooks'):
        names += '/' + webhook.get('command_name') + '\n'
    return names

def get_webhook_handler(webhook):
    def webhook_handler(bot, update):
        post_json(logger, webhook, update)

    return webhook_handler

def setup_webhooks(dp):
    for webhook in config.get('webhooks'):
        hook_handler = CommandHandler(webhook.get('command_name'), get_webhook_handler(webhook))
        dp.add_handler(hook_handler)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=config.get('bot_token'))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Static command handlers
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)

    # setup handlers
    dp.add_handler(start_handler)
    dp.add_handler(help_handler)

    setup_webhooks(dp)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    logger.info('Bot started')

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

