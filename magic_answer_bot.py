#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from time import sleep
import numpy as np

#here is our answers
greetings = ['привет, {}', 'Привет, {}!', 'Привет!', 'Здравствуй, {}', 'ой, привет','привет', 'Hola']
morning = ['Доброе утро!' , 'доброе утро)', 'Доброе утро, {})']
night = ['ты так поздно пишешь, {}. спать пора же']

yes = ['да', 'Да!', 'Конечно, {}', 'Давай', 'Прекрасно', 'звучит хорошо',
       'Не могу сказать точно, но есть все шансы',
       'ладно', 'хорошо', 'с тобой, {}, куда угодно', 'как раз думала об этом']

no = ['нет','Ни за что и никогда!','с тобой, {}, нет', 'в другой раз', 'думаю, нет', 'в другой раз', 'не хочу',
      '{}, я очень занята', 'я бы с удовольствием но нет', 'мне бы не хотелось, {}', 'нет конечно', 'Nope', 'No']

i_do_not_know = ['не знаю пока, {}', 'не могу сказать, спроси попозже', 'возможно', 'я подумаю','{}, подумай и реши']

answers = []
answers.extend(yes)
answers.extend(no)
answers.extend(i_do_not_know)

morning_greetings = greetings + morning
night_greetings = greetings + night

users_logger = {}

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError  # python 2


def main():

    bot = telegram.Bot('145650753:AAFvt7VBBgtiyqZzF5hZMeX-Ts3HK8i3lfw')

    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            update_id = answer_upg(bot, update_id)
        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            elif e.message == "Unauthorized":
                # The user has removed or blocked the bot.
                update_id += 1
            else:
                raise e
        except URLError as e:
            # These are network problems on our end.
            sleep(1)

def answer_upg(bot, update_id):
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
        message = update.message.text
        name_of_person = (update.message.from_user.first_name)
        person = '{} {}'.format(update.message.from_user.first_name, update.message.from_user.last_name)
        current_date = (update.message.date.date())
        current_time = (update.message.date.time())

        greet = False
        if message:
            if person not in users_logger.keys():
                users_logger[person] = {}
                users_logger[person][current_date] = False #magic_state
                greet = True
            elif current_date not in users_logger[person].keys():
                users_logger[person][current_date] = False
                greet = True
            else:
                greet = False

            if message == 'magic':
                users_logger[person][current_date] = True

            magic = users_logger[person][current_date]
            if greet:
                if (6 <= current_time.hour<= 12):
                    answer = np.random.choice(morning_greetings)
                elif (2 <= current_time.hour<= 5):
                    answer = np.random.choice(night_greetings)
                else:
                    answer = np.random.choice(greetings)
            elif magic:
                answer = np.random.choice(yes)
            else:
                answer = np.random.choice(answers)

            if '{}' in answer:
                answer = answer.format(name_of_person)
            bot.sendMessage(chat_id=chat_id, text=answer)
    return update_id

if __name__ == '__main__':
    main()
