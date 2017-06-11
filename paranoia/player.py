import logging
import random
import string

from django_paranoiabot.models import (
    Player,
)

from .decorators import (
    admin_only,
    silent_in_group
)
from .util import (
    log_message
)

logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

"""
    This file contains some player related bot command handlers and helpers
"""

MESSAGES = {
    'cheating_negative': 'Player {} tried to cheat by spending a negative amount of {}',
    'cheating_too_much': 'Player {} tried to spend {} pp',
    'spent': 'Player {} spent {} {}',
    'cannot_spend': 'I cannot spend {} when you don\'t specify the amount'
}


@silent_in_group
def spend_pp(bot, update, args):
    _spend('pp', bot, update, args)


@silent_in_group
def spend_credits(bot, update, args):
    _spend('credits', bot, update, args)


def _spend(type, bot, update, args):
    current_player = Player.objects.filter(telegram_id=update.message.from_user.id).first()
    if len(args) != 1:
        update.message.reply_text(MESSAGES['cannot_spend'].format(type))
    else:
        amount = int(args[0])
        if amount < 0:
            log_message(bot, MESSAGES['cheating_negative'].format(current_player.get_player_name(), type))
            amount *= -1
        if type == 'pp':
            if amount > 5:
                log_message(bot, MESSAGES['cheating_too_much'].format(current_player.get_player_name(), amount))
                update.message.reply_text('Reset PP to the maximum of five. Incident reported')
                amount = 5
            current_player.remove_pp(amount)
        elif type == 'credits':
            current_player.remove_credits(amount)
        else:
            logger.error('Something went wrong, type was: {}'.format(type))
        current_player.save()
        log_message(bot, MESSAGES['spent'].format(current_player.get_player_name(), amount, type))


@silent_in_group
def info(bot, update):
    current_player = Player.objects.filter(telegram_id=update.message.from_user.id).first()
    info_message = """
Name: {}
Clearance: {}
Credits: {}
PP: {}
    """.format(
        current_player.get_player_name(),
        current_player.clearance.name,
        current_player.credits,
        current_player.pp
    )
    update.message.reply_text(info_message)
