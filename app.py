import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValueConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def welcome(message):
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")


@bot.message_handler(commands=['help', ])
def help(message: telebot.types.Message):
    text = "Команды бота: /help, /values \n Чтобы конвертировать валюту введите: <Название начальной валюты> <Название искомой валюты> <Количество начальной валюты>"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n" .join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')
        if len(values_) != 3:
            raise ConvertionException('Неправильное количество параметров!')
        quote, base, amount = values_
        price = ValueConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} равна {price}'
        bot.send_message(message.chat.id, text)


bot.polling()
