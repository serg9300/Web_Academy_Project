from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import User, Update, ParseMode, Sticker
import apiai, json
import requests
import re

updater = Updater(token='809239472:AAHfJIy7O9EFJT7IKbdI5jpxWZ5plCJaCuU')
#sticker_id = 'CAADAgADqggAAgi3GQIQO4YOkKiCCQI'
dispatcher = updater.dispatcher

def startCommand(main, update):
    main.send_message(chat_id=update.message.chat_id, text=('Hi, ' + update.message.chat.first_name))

def helpCommand(main, update):
    main.send_message(chat_id=update.message.chat_id,
                      text = (
                          '<b>List of commands:\n\n</b>'
                          '/start - Starting chat\n'
                          '/doggy - Receive funny photo with dog\n'
                          '/help - Help'),
                      parse_mode=ParseMode.HTML)


def textMessage(main, update):
    request = apiai.ApiAI('9f8abd0126b8423ba015757ae7d70aad').text_request() # Токен API к Dialogflow
    request.lang = 'en' # На каком языке будет послан запрос
    request.session_id = 'serg9300_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        main.send_message(chat_id=update.message.chat_id, text=response)
    else:
        main.send_message(chat_id=update.message.chat_id, text='I do not understand, please type again')

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search('([^.]*)$',url).group(1).lower()
    return url
def doggy(doggy, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    doggy.send_photo(chat_id=chat_id, photo=url)

# def reply_sticker(main, update):
#     main.send_sticker(chat_id=update.message.chat_id, sticker_id=sticker_id)
def main():
    dispatcher.add_handler(CommandHandler('start', startCommand))
    dispatcher.add_handler(CommandHandler('help', helpCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, textMessage))
    dispatcher.add_handler(CommandHandler('doggy',doggy))
    updater.start_polling(clean=True, timeout=10)
    updater.idle()

if __name__ == '__main__':
    main()