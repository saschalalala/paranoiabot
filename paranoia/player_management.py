import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ConversationHandler

from django_paranoiabot.models import Player

logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


"""
    This file contains all functions that are necessary for clone management functionality
"""


def clone_kill(bot, update, user_data):
    query = update.callback_query
    player = Player.objects.filter(telegram_id=query.data).first()
    player.increment_clone()
    player.save()
    bot.edit_message_text(text='Clone killed',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          )
    bot.send_message(player.telegram_id, 'One of your clones has been killed')
    return ConversationHandler.END


def name_change(bot, update, user_data):
    query = update.callback_query
    user_data['telegram_id'] = query.data
    bot.edit_message_text(text='Please enter the custom player name or <reset> (without <>) to reset it',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    return 1


def name_save(bot, update, user_data):
    custom_name = update.message.text
    if custom_name == 'reset':
        custom_name = ""
    try:
        player = Player.objects.filter(telegram_id=user_data['telegram_id']).first()
        player.set_custom_player_name(custom_name)
        player.save()
        update.message.reply_text('Name changed to {}'.format(player.get_player_name()))
    except:
        update.message.reply_text('Invalid input or not implemented. Aborting.')
    return ConversationHandler.END


def admin_spend_choose_type(bot, update, user_data):
    query = update.callback_query
    user_data['telegram_id'] = query.data
    inline_keyboard = [
        [
            InlineKeyboardButton('PP', callback_data='pp'),
            InlineKeyboardButton('Credits', callback_data='credits'),
        ]
    ]
    bot.edit_message_text(text='Choose what type you want to spend for the player',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=InlineKeyboardMarkup(inline_keyboard))
    return 1


def admin_spend_choose_amount(bot, update, user_data):
    query = update.callback_query
    user_data['spending_type'] = query.data
    bot.edit_message_text('Choose the amount (positive or negative)',
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          )
    return 2


def admin_spend_wrapper(bot, update, user_data):
    user_data['amount'] = update.message.text
    return _admin_spend_save(user_data['spending_type'],
                             user_data['telegram_id'],
                             user_data['amount'],
                             bot,
                             update)


def _admin_spend_save(type, player, amount, bot, update):
    try:
        chosen_player = Player.objects.filter(telegram_id=player).first()
    except ValueError:
        update.message.reply_text('Cannot get player with this ID')
        return ConversationHandler.END
    amount = int(amount)
    if type == 'pp':
        try:
            chosen_player.remove_pp(amount)
            chosen_player.save()
        except:
            update.message.reply_text('Invalid input or not implemented. Aborting.')
            return ConversationHandler.END
    elif type == 'credits':
        try:
            chosen_player.remove_credits(amount)
            chosen_player.save()
        except:
            update.message.reply_text('Invalid input or not implemented. Aborting.')
            return ConversationHandler.END
    update.message.reply_text('Successfully spent {} {} for {}'.format(amount, type, chosen_player.get_player_name()))
    bot.send_message(chosen_player.telegram_id, '{} {} have been spent for you'.format(amount, type))
    return ConversationHandler.END


def admin_info(bot, update):
    info_message = "`{0: <7} {1: >7} {2: >5}`"
    info_messages = [""]
    # try:
    all_players = Player.objects.filter(gm=False).all().order_by('name')
    for player in all_players:
        info_messages.append(info_message.format(
            player.name,
            player.credits,
            player.pp)
        )
    message = "\n".join(info_messages)
    update.message.reply_text(message, parse_mode="Markdown")
    # except:
    #     update.message.reply_text(text='Invalid input or not implemented. Aborting.')