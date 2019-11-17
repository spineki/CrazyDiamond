import telebot
from telebot import types, util

import threading
from core import Core
token = "1059380368:AAEDnyas0jxbZQ-wnVPXVURNKvmdku81wJc"
chat_id = 948171594
bot = telebot.TeleBot(token)
bot.send_message(chat_id, "Awakening my Masters...")

core = Core()
current_category = None
current_engine = None

bot.send_message(chat_id, "Done!")

#bot.send_message(chat_id=chat_id, text="*bold* Example message",
#                parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=["start"])
def choosing_category(message):
    markup = types.InlineKeyboardMarkup()
    for category in core.engines:
        item_btn=types.InlineKeyboardButton(category, callback_data= "#category " + category )
        markup.row(item_btn)
    bot.reply_to(message, "Which category do you wanna use? ", reply_markup=markup)

@bot.callback_query_handler(lambda query: "#category" in query.data.split(" ", 1))
def choosing_engine(query):
    query.data = query.data.split(" ", 1)[-1]
    markup = types.InlineKeyboardMarkup()
    current_category = query.data
    for engine in core.engines[current_category]:
        item_btn=types.InlineKeyboardButton(engine.name, callback_data="#engine " + engine.name)
        markup.row(item_btn)
    bot.reply_to(query.message, "In the category *" + current_category
                 + "*, which engine do you want to use? ", parse_mode="Markdown",
                 reply_markup=markup)



@bot.callback_query_handler(lambda query: "#engine" in query.data.split(" ", 1) )
def using_engine(query):
    query.data = query.data.split(" ", 1)[-1]
    for engine in core.get_all_engines():
        if engine.name == query.data:
            current_engine = engine
            break
    bot.reply_to(query.message, "You need to fulfill some args in order to launch " + current_engine.name +"engine.")
    print("will use " + str(query.data))



bot.polling()