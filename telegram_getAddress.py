##
# Bot to obtain the address to bind the notifications after.
# User:
#   Execute this bot the first time and search with the bot id.
#   !IMPORTANT! Replace the token with your bot token
##
import telebot

bot = telebot.TeleBot("224952481:AAHmbCQfgAkROv5Dxcaf8YVlXGrG00u7oEs")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the delegate bot.\nPlease, execute /address to get your id for the config.json file configuration")


@bot.message_handler(commands=["address"], func=lambda message: True)
def echo_all(message):
    print(message.chat.id)
    response_msg = "This is your address for config.json: " + str(message.chat.id)
    bot.send_message(message.chat.id, response_msg)

## Iddle. Stop the proccess when you need
bot.polling()