import logging

from django_paranoiabot.models import (
    Game,
    Player
)

logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


"""
    This file contains some utilty functions
"""


def log_to_channel(bot, update):
    message = "{}: {}".format(update.message.from_user['username'], update.message.text)
    log_channel_id = Game.objects.get(pk=1).channel_id
    bot.sendMessage(log_channel_id, message)


def log_message(bot, message):
    log_channel_id = Game.objects.get(pk=1).channel_id
    bot.sendMessage(log_channel_id, message)


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))


def fallback_senseless_recipient(bot, update):
    pass


def send_message_to_everyone(bot, message):
    send_message(bot, 'everyone', message)


def send_message(bot, recipient, message):
    if recipient == 'everyone':
        all_players = Player.objects.filter(gm=False)
        for player in all_players:
            bot.send_message(player.telegram_id, message)
    else:
        bot.send_message(recipient, message)


def forward_message(update, recipient):
    if recipient == 'everyone':
        all_players = Player.objects.filter(gm=False)
        for player in all_players:
            update.message.forward(player.telegram_id)
        update.message.reply_text('Message forwarded to all players')
    else:
        recipient_name = Player.objects.filter(telegram_id=recipient).first().get_player_name()
        update.message.forward(recipient)
        update.message.reply_text('Message forwarded to {}'.format(recipient_name))