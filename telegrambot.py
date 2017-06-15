import datetime as dt
import logging

from django_telegrambot.apps import DjangoTelegramBot

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters
)

from .paranoia.player_management import (
    admin_info,
    admin_spend_choose_type,
    admin_spend_choose_amount,
    admin_spend_wrapper,
    clone_kill,
    name_change,
    name_save,
)
from .paranoia.conversation_management import (
    cancel,
    choose_user
)
from .paranoia.misc import (
    bot_help,
    greet_everyone,
    random_home
)
from .paranoia.player import(
    info,
    spend_credits,
    spend_pp
)
from .paranoia.snippets import (
    add_text_snippet,
    message_create,
    message_send,
    reply,
    snippet_send,
    snippet_choose
)
from .paranoia.util import (
    log_to_channel,
    error
)


logging.basicConfig(format='[%(asctime)s - %(name)s - %(funcName)s -  %(levelname)s]: %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

Globals = {}


def main():
    logger.info('starting')
    dp = DjangoTelegramBot.dispatcher
    cancel_handler = CommandHandler('cancel', cancel)
    help_handler = CommandHandler('help', bot_help)
    # admin_conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('admin', admin)],
    #     states={
    #
    #     },
    #     fallbacks=[cancel_handler]
    # )
    greet_everyone_handler = CommandHandler('greet_everyone', greet_everyone)
    text_snippet_handler = CommandHandler('add_text_snippet', add_text_snippet, pass_args=True)
    reply_handler = CommandHandler('reply', reply, pass_args=True)
    random_home_handler = CommandHandler('random_home', random_home)
    send_snippet_handler = ConversationHandler(
        entry_points=[CommandHandler('send_snippet', choose_user)],
        states={
            0: [CallbackQueryHandler(snippet_choose, pass_user_data=True)],
            1: [CallbackQueryHandler(snippet_send, pass_user_data=True)],
        },
        fallbacks=[cancel_handler]
    )
    send_custom_message_handler = ConversationHandler(
        entry_points=[CommandHandler('send_message', choose_user)],
        states={
            0: [CallbackQueryHandler(message_create, pass_user_data=True)],
            1: [MessageHandler(Filters.all, message_send, pass_user_data=True)]
        },
        fallbacks=[cancel_handler]
    )
    clone_handler = ConversationHandler(
        entry_points=[CommandHandler('kill_clone', choose_user)],
        states={
            0: [CallbackQueryHandler(clone_kill, pass_user_data=True)]
        },
        fallbacks=[cancel_handler]
    )
    name_change_handler = ConversationHandler(
        entry_points=[CommandHandler('change_name', choose_user)],
        states={
            0: [CallbackQueryHandler(name_change, pass_user_data=True)],
            1: [MessageHandler(Filters.text, name_save, pass_user_data=True)]
        },
        fallbacks=[cancel_handler]
    )
    spend_handler = ConversationHandler(
        entry_points=[CommandHandler('spend', choose_user)],
        states={
            0: [CallbackQueryHandler(admin_spend_choose_type, pass_user_data=True)],
            1: [CallbackQueryHandler(admin_spend_choose_amount, pass_user_data=True)],
            2: [MessageHandler(Filters.text, admin_spend_wrapper, pass_user_data=True)]
        },
        fallbacks=[cancel_handler]
    )
    admin_info_handler = ConversationHandler(
        entry_points=[CommandHandler('admin_info', choose_user)],
        states={
            0: [CallbackQueryHandler(admin_info, pass_user_data=True)]
        },
        fallbacks=[cancel_handler]
    )

    log_message_handler = MessageHandler(Filters.all, log_to_channel)

    # Player specific handlers
    info_handler = CommandHandler('info', info)
    spend_credits_handler = CommandHandler('spend_credits', spend_credits, pass_args=True)
    spend_pp_handler = CommandHandler('spend_pp', spend_pp, pass_args=True)

    dp.add_handler(info_handler)
    dp.add_handler(spend_credits_handler)
    dp.add_handler(spend_pp_handler)

    # Handler registrations
    # Simple handlers
    dp.add_handler(greet_everyone_handler)
    dp.add_handler(text_snippet_handler)
    dp.add_handler(random_home_handler)
    dp.add_handler(help_handler)
    dp.add_handler(reply_handler)

    # Conversation handlers
    dp.add_handler(send_snippet_handler)
    dp.add_handler(clone_handler)
    dp.add_handler(send_custom_message_handler)
    dp.add_handler(name_change_handler)
    dp.add_handler(spend_handler)
    dp.add_handler(admin_info_handler)



    dp.add_handler(log_message_handler)

    # dp.add_handler(simple_test_handler)

    dp.add_error_handler(error)