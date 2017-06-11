import logging
import random
import string

from django_paranoiabot.models import (
    Player,
    Game,
    Snippet
)

from .decorators import (
    admin_only,
    silent_in_group
)
from .util import (
    send_message_to_everyone,
    log_to_channel
)

logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

"""
    This file contains some miscellaneous bot command handlers and helpers
"""


@admin_only
def greet_everyone(bot, update):
    greeting_message = Snippet.objects.filter(key="greeting").first()

    if greeting_message is None:
        logger.error("Greeting message doesn't exist")
        update.message.reply_text('The greet message is not defined yet, please fix this.')
    else:
        send_message_to_everyone(bot, greeting_message.value)


@silent_in_group
def bot_help(bot, update):
    current_player = Player.objects.filter(telegram_id=update.message.from_user.id).first()
    if not current_player.gm:
        help_text = """
I'm not here to help you.
Okay, there are some things you can ask me to do for you.
Type /spend_pp <number> to spend some pp.
Type /spend_credits <number> to spend some credits.
Type /info for some information about your current status
"""

    else:
        help_text = """
Type /help for a list of commands       
Type /admin_info to get some infos about the players
Type /add_text_snippet key value to add text snippets
Type /kill_clone to kill a clone
Type /send_snippet to send a snippet
Type /send_message to send a message (Will be forwarded, so use text snippets for text whenever possible)
Type /change_name to set a custom player name
Type /random_home 'roll a home area dice'
Type /spend to spend pp or credits 
"""
    update.message.reply_text(help_text)


@admin_only
def set_name(bot, update):
    # wrong position, needs a conversation handler
    pass


@admin_only
def random_home(bot, update):
    home = "".join([random.choice(string.ascii_letters).upper() for _ in range(3)])
    update.message.reply_text(home)



