#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import tweepy
import logging
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!, this bot will give you video link from twitter')

def parse(bot, update):
    text = update.message.text
    tweet_id = re.match(r'https:\/\/twitter\.com\/(\w+)\/status\/(\d+)',text).group(2)
    tweet = api.get_status(tweet_id)

    if 'media' in tweet.entities:
        test = tweet.extended_entities['media'][0]['type']
        if test == 'photo':
            photo_url = tweet.entities['media'][0]['media_url_https'] + ":orig"
        else:
            A = tweet.extended_entities['media'][0]['video_info']['variants']
            variable = max([d for d in A if ('bitrate') in d ],key=lambda x:x['bitrate'])
            photo_url = variable['url']
    else:
        photo_url = "Twitter media cannot be found!"

    update.message.reply_text(photo_url)
    bot.sendDocument(chat_id=update.message.chat_id,document=photo_url)
    # print(photo_url)
    update.message.reply_video(photo_url)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def echo(bot, update):
    update.message.reply_text("Tweet id cannot be found!")


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(RegexHandler(r'https:\/\/twitter\.com\/(\w+)\/status\/(\d+)', parse))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
