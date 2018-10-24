from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler, CommandHandler
import chat

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

REQUEST_KWARGS={
    'proxy_url': 'http://159.69.203.124:9999',
}


if __name__ == '__main__':
    chat.load_user_data()
    updater = Updater(token='703010342:AAFsI5OC6hdp9hhLKayshOYJskYl862SXoY', request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(chat.join_to_event, pattern='^join:'))
    dispatcher.add_handler(CallbackQueryHandler(chat.leave_from_event, pattern='^leave:'))
    dispatcher.add_handler(CallbackQueryHandler(chat.show_location_event, pattern='^map:'))
    dispatcher.add_handler(CallbackQueryHandler(chat.delete_event, pattern='^delete:'))
    dispatcher.add_handler(MessageHandler(Filters.location, chat.input))
    dispatcher.add_handler(MessageHandler(Filters.text, chat.input))
    dispatcher.add_handler(CommandHandler('cancel', chat.cancel))
    dispatcher.add_handler(CommandHandler('start', chat.start))
    dispatcher.add_handler(CommandHandler('register', chat.register, pass_args=True))
    dispatcher.add_handler(CommandHandler('login', chat.login, pass_args=True))
    dispatcher.add_handler(CommandHandler('create_event', chat.request_for_creating_event))
    dispatcher.add_handler(CommandHandler('list_all_events', chat.request_for_list_events))
    dispatcher.add_handler(CommandHandler('list_my_events', chat.request_for_list_your_events))

    updater.start_polling()
