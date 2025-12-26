import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате: \n<имя валюты, цену которой он хочет узнать>  \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>. \
\n При вводе команды /start или /help выводятся инструкции по применению бота. \
\n При вводе команды /values выводится информация о всех доступных валютах.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для конвертации валюты:'
    for key in keys.keys():
        text = '\n - '.join((text, key,))
    bot.reply_to(message, text)
    
    

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    message.text = message.text.lower()
    try:
        values = message.text.split(' ')
            
        if len(values) != 3:
            raise ConvertionException('Не верное количество входных параметров!')
            
        quote, base, amount = values
        
        total_base = CryptoConverter.get_price(quote, base, amount)
        total_cbr = CryptoConverter.cbr_price(quote, base, amount)    
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'coindesk.com: Цена {amount} {quote} в {base} = {round(total_base, 4)} \
    \nПо курсу ЦБР: Цена {amount} {quote} в {base} = {round(total_cbr, 4)}'
        bot.send_message(message.chat.id, text)


bot.polling()