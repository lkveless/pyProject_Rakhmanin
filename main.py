import telebot
from Constants import bot_key

bot = telebot.TeleBot(bot_key)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Приветствую, для дальнейшей работы введите какой-либо текст")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.chat.id, "Здравствуйте, что Вы хотели?")


bot.polling()
