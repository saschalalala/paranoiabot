import logging

from django_paranoiabot.models import (
    Game,
    Player
)

logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

"""
    This file contains all decorator functionality
"""


def admin_only(func):
    def check_permissions(*args, **kwargs):
        bot = args[0]
        update = args[1]
        current_user = Player.objects.filter(telegram_id=update.message.from_user.id).first()
        if not current_user.gm:
            update.message.reply_text("You are not allowed to do this, Troubleshooter. This incident will be reported")
            message = "The user {} just entered a forbidden command.".format(current_user)
            log_channel_id = Game.objects.get(pk=1).channel_id
            bot.sendMessage(log_channel_id, message)
            return 1
        return func(*args, **kwargs)
    return check_permissions


def silent_in_group(func):
    def dont_process_commands_from_groups(*args, **kwargs):
        bot = args[0]
        update = args[1]
        if update.message.chat.id < 0:
            current_user = update.message.from_user
            bot.send_message(current_user.id, 'Commands from group chats are not supported, please repeat')
            return 1
        return func(*args, **kwargs)
    return dont_process_commands_from_groups