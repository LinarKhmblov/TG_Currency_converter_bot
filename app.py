import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def help(message: telebot.types.Message):
    text = f'{message.chat.username}, добро пожаловать в приложение "Конвертер валют"! \nДля начала работы с ботом, введите команду в следующем формате: ' \
           f'\n<имя валюты> ' \
           '\n<в какую валюту перевести> ' \
           '\n<количество переводимой валюты> через пробел. ' \
           '\nДля получения списка доступных валют, используй команду /values. ' \
           '\nДля вызова информационной справки по работе с ботом используй команду /help.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help', ])
def value(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты> через пробел.\nПример ввода: доллар рубль 10.\nЧтобы увидеть список всех доступных валют, введите команду /values.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Введите три параметра, либо вызовите справку /help.'

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f' {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
