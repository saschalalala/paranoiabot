import logging

from django.db import IntegrityError
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ConversationHandler

from django_paranoiabot.models import(
    Player,
    Snippet
)
from .decorators import admin_only
from .util import (
    forward_message,
    send_message
)

logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

"""
    This file contains all functions that are necessary for snippet and message sending functionality
"""


@admin_only
def add_text_snippet(bot, update, args):
    if len(args) < 2:
        update.message.reply_text('I need a key and a string')
    else:
        key = args[0][:20]
        value = " ".join(args[1:])
        snippet = Snippet(key=key,
                          value=value,
                          added_by=update.message.from_user.id,
                          added_via="Telegram")
        try:
            snippet.save()
        except IntegrityError:
            update.message.reply_text('I\'m afraid I cannot do this')
            logger.warn('Trying to add an existing key')


def snippet_choose(bot, update, user_data):
    query = update.callback_query
    user_data['recipient'] = query.data
    snippets = Snippet.objects.all()
    inline_keyboard = []
    for snippet in snippets:
        button = InlineKeyboardButton(snippet.key, callback_data=str(snippet.key))
        inline_keyboard.append([button])
    bot.edit_message_text(text='Choose snippet',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=InlineKeyboardMarkup(inline_keyboard))
    return 1


def snippet_send(bot, update, user_data):
    query = update.callback_query
    chosen_snippet = Snippet.objects.filter(key=query.data).first()
    user_data['text'] = chosen_snippet.value
    send_message(bot, user_data['recipient'], user_data['text'])
    bot.edit_message_text(text='Message successfully sent',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          )
    return ConversationHandler.END


def message_create(bot, update, user_data):
    query = update.callback_query
    user_data['recipient'] = query.data
    bot.edit_message_text(text='Please upload the image or file or type the text you want to send',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    return 1


def message_send(bot, update, user_data):
    recipient = user_data['recipient']
    thing_to_send = ""
    if update.message.text:
        thing_to_send = update.message.text
        message_type = "text"
    elif update.message.document:
        thing_to_send = update.message.document
        message_type = "doc"
    elif update.message.photo:
        thing_to_send = update.message.photo[-1]
        message_type = "photo"
    elif update.message.sticker:
        thing_to_send = update.message.sticker
        message_type = "sticker"
    else:
        message_type = "unknown"
    message = thing_to_send
    logger.debug(message)
    logger.debug(message_type)
    send_message(bot, recipient, thing_to_send, message_type=message_type)
    return ConversationHandler.END


@admin_only
def reply(bot, update, args):
    if len(args) < 2:
        update.message.reply_text('I need a recipient and a string to send')
    else:
        recipient = Player.objects.filter(name=args[0]).first().telegram_id
        message = " ".join(args[1:])
        bot.send_message(recipient, message)
        update.message.reply_text('Successfully replied')
