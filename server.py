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
current_task = None
current_function = None
current_data = None

def query_to_message(query):
    if hasattr(query,"data"): # the query is a real query
        return query.message, query.data
    else:
        # we need to use the shared query
        return query, current_data # because query is a message


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
    global current_category
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
    global current_engine
    global current_task
    query.data = query.data.split(" ", 1)[-1]
    for engine in core.get_all_engines():
        if engine.name == query.data:
            current_engine = engine
            break
    bot.reply_to(query.message, "You need to fulfill some args in order to launch " + current_engine.name +"engine.")
    # now, with have an engine object in current_object
    # if we modify the current_object, we modify directly the core.engines[i] linked object.
    # but it's quite messy
    current_task = current_engine.get_task_template()
    # here we launch the using argument function. but we need to pass a query argument.
    # to make it easy, we just take the
    query.data = "#argument #0"

    using_arguments(query)




@bot.callback_query_handler(lambda query: "#arguments" in query.data.split(" ", 1) )
def using_arguments(query):
    # first, we get a good message and data form
    message, data = query_to_message(query)
    # We save the indice of the current argument that need to be filled for the engine.
    argument_indice = int(data.split(" ", 1)[-1][1:]) # [1:] to get rid of the hashtag

    if argument_indice >= len(current_task):
        choosing_send(query)
        return
    current_argument = current_task[argument_indice]
    #bot.edit_message_text("text random",chat_id,query.message.message_id)

    keyword = current_argument["keyword"]
    description =  current_argument["description"]
    text = keyword + "\n" + description

    bot.reply_to(message, text)
    # Then, we tell the next function that need to be called is using_argument, to use the following indice
    global current_function
    current_function = using_arguments
    # and we give the number of the next indice.
    global current_data
    current_data = "#argument #" + str(argument_indice + 1)

    print("nikoumouk")

@bot.callback_query_handler(lambda query: "#choosing_send" in query.data)
def choosing_send(query):
    # first, we get a good message and data form
    message, data = query_to_message(query)
    markup = types.InlineKeyboardMarkup()

    # here, possible to add add a custom recap of the task, with the possibility to edit the task
    item_btn = types.InlineKeyboardButton("Yes!", callback_data="#sending_task " + "#yes")
    markup.row(item_btn)
    item_btn = types.InlineKeyboardButton("No!", callback_data="#sending_task " + "#no")
    markup.row(item_btn)
    bot.reply_to(message, "The task is ready to go. Do you really want to send it?", reply_markup=markup)



@bot.callback_query_handler(lambda query: "#sending_task" in query.data)
def sending_task(query):
    # first, we get a good message and data form
    message, data = query_to_message(query)
    choice = data.split(" ", 1)[-1]
    if choice == "#yes":
        print("sending to the core")
    else:
        print("aborting")
    # We save the indice of the current argument that need to be filled for the engine.





@bot.message_handler(content_types=["text"])
def react_to_text(message):
    bot.reply_to(message," Let's see that...")
    global current_engine
    global current_task
    global current_data
    global current_function

    if current_function != None:
        new_function = current_function
        current_function = None

        new_function(message) # to avoid concurency access that will never change current_function
    else:
        current_engine = core.get_reacting_motor(message.text)
        bot.reply_to(message, "The engine *" + current_engine.name + "* can handle your request", parse_mode="Markdown")
        current_task =  current_engine.get_minimal_task_template()
        current_data = "#argument #0"
        using_arguments(message)






print("start bot pooling")

bot.polling()

