import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import ConversationHandler

from .decorators import admin_only
from django_paranoiabot.models import (
    Player
)

logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
"""
    This file contains some conversation management functions
"""


@admin_only
def choose_user(bot, update):
    inline_keyboard = []
    recipients = Player.objects.filter(gm=False).all()
    for recipient in recipients:
        button = InlineKeyboardButton(recipient.get_player_name(), callback_data=str(recipient.telegram_id))
        inline_keyboard.append([button])
    inline_keyboard.append([
        InlineKeyboardButton("Everyone (In Private)", callback_data='everyone'),
        # InlineKeyboardButton("Specific clearance", callback_data='clearance'),
        InlineKeyboardButton("Chat group", callback_data='-245325242'),
    ])
    update.message.reply_text('Choose user',
          reply_markup=InlineKeyboardMarkup(inline_keyboard))
    return 0


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Canceled the current operation',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
