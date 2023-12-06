import telebot
from config import keys, TOKEN
from extensions import ConvertionException, APIException

print("Telegram bot is ready")
bot = telebot.TeleBot(TOKEN)

# Обрабатываются команды '/start' or '/help' справочной информацией
@bot.message_handler(commands=['start', 'help'])
def helps(message: telebot.types.Message):
    text = "Что бы начать работу, ведите запрос в следующем формате: \n " \
           "<название валюты> <в какую валюту перевести> <сколько перевести>. \n" \
           "Для вывода доступных валют напишите команду /values ."
    bot.reply_to(message, text)
# Обрабатываются команды '/values' выводом доступных валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
#count
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        vals = message.text.split(' ')

        if len(vals) != 3:  # обработка ошибки ввода избыточных параметров при вводе
            raise ConvertionException('Необходимо именно 3 параметра: <валюта> <валюта> <число>')

        quote, base, amount = vals
        total_base = APIException.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()