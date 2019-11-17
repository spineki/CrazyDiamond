import telebot
from telebot import types, util
import threading
from core import Core
token = "1059380368:AAEDnyas0jxbZQ-wnVPXVURNKvmdku81wJc"
chat_id = 948171594
bot = telebot.TeleBot(token)

core = Core()

bot.send_message(chat_id, "Awakening my Masters...")
bot.send_message(chat_id, "Done!")

#bot.send_message(chat_id=chat_id, text="*bold* Example message",
#                parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=["start"])
def choosing_category(message):
    markup = types.InlineKeyboardMarkup()
    for category in core.engines:
        item_btn=types.InlineKeyboardButton(category, callback_data= category )
        markup.row(item_btn)
    bot.reply_to(message, "Which categorie do you wanna use?: ", reply_markup=markup)

@bot.callback_query_handler(lambda query: query.data in core.engines)
def choosing_engine(query):
    markup = types.InlineKeyboardMarkup()
    category = query.data
    for engine in core.engines[category]:
        item_btn=types.InlineKeyboardButton(engine.name, callback_data=engine.name)
        markup.row(item_btn)
    bot.reply_to(query.message, "Which engine do you wanna use?: ", reply_markup=markup)



@bot.callback_query_handler(lambda query: query.data in [engine.name for engine in core.get_all_engines()]  )
def using_engine(query):
    engine  = [engine.name for engine in core.get_all_engines()]
    print("will use " + str(query.data))

bot.polling()