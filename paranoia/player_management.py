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
    return ConversationHandler.END


def admin_info(bot, update, user_data):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_data['telegram_id'] = query.data
    info_message = """
Name: {}
Clearance: {}
Credits: {}
PP: {}
        """
    if user_data['telegram_id'] == 'everyone':
        all_players = Player.objects.filter(gm=False)
        for player in all_players:
            bot.send_message(chat_id, info_message.format(
                                      player.get_player_name(),
                                      player.clearance.name,
                                      player.credits,
                                      player.pp))
    else:
        try:
            current_player = Player.objects.filter(telegram_id=user_data['telegram_id']).first()
            bot.send_message(chat_id, info_message.format(
                                      current_player.get_player_name(),
                                      current_player.clearance.name,
                                      current_player.credits,
                                      current_player.pp))
        except:
            bot.send_message(chat_id, text='Invalid input or not implemented. Aborting.')
    return ConversationHandler.END







