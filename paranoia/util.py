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
    if update.message.chat.id > 0:
        log_channel_id = Game.objects.get(pk=1).channel_id
        player = Player.objects.filter(telegram_id=update.message.from_user.id).first()
        forward_message(update, log_channel_id)
        reply_snippet = "/reply {}".format(player.name)
        bot.send_message(log_channel_id, reply_snippet)


def log_message(bot, message):
    log_channel_id = Game.objects.get(pk=1).channel_id
    bot.send_message(log_channel_id, message)


def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))


def fallback_senseless_recipient(bot, update):
    pass


def send_message_to_everyone(bot, message):
    send_message(bot, 'everyone', message)


def send_message(bot, recipient, message, **kwargs):
    send_function = bot.send_message
    if kwargs:
        message_type = kwargs['message_type']
        if message_type == "text":
            send_function = bot.send_message
        elif message_type == "doc":
            message = bot.get_file(message.file_id)
            send_function = bot.send_document
        elif message_type == "sticker":
            message = message['file_id']
            send_function = bot.send_sticker
        elif message_type == "photo":
            # message = message['file_id']
            message = message.file_id
            send_function = bot.send_photo
        elif message_type == "unknown":
            return -1
    logger.debug(send_function)
    logger.debug(kwargs)
    if recipient == 'everyone':
        all_players = Player.objects.filter(gm=False)
        for player in all_players:
            send_function(player.telegram_id, message)
    else:
        send_function(recipient, message)


def forward_message(update, recipient):
    if recipient == 'everyone':
        all_players = Player.objects.filter(gm=False)
        for player in all_players:
            update.message.forward(player.telegram_id)
        update.message.reply_text('Message forwarded to all players')
    else:
        try:
            recipient_name = Player.objects.filter(telegram_id=recipient).first().name
            update.message.forward(recipient)
            # update.message.reply_text('Message forwarded to {}'.format(recipient_name))
        except:
            update.message.forward(recipient)
            # update.message.reply_text('Message forwarded to the group')


