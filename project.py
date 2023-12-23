import telebot
import config
from time import sleep
from datetime import datetime, time


if __name__ == "__main__":
    time_for_not = "14"
    bot = telebot.TeleBot(config.token)

    @bot.message_handler(commands=["start"])
    def welcome(msg):
        text = """Привет. Я бот - твой помощник в изучении английского языка. 
        С помощью команды /set_time установи время, в которое я тебе буду напоминать о том, что пора учить слова. 
        По умолчанию, я буду отправлять уведомление в 14 часов
        С помощью команды /start_scheduling бот начнет отправлять уведомления в заданное время"""

        bot.send_message(msg.chat.id, text)

    @bot.message_handler(commands=["set_time"])
    def set_time(msg):
        global time_for_not
        message_to_send = f"Текущее время выбрано: {time_for_not}:00"
        new_massage = (
            f"Введите час (от 0 до 23), когда вы хотели бы получать уведомления"
        )
        bot.send_message(msg.chat.id, message_to_send)
        bot.send_message(msg.chat.id, new_massage)
        bot.register_next_step_handler(msg, time_from_user)

    def time_from_user(msg):
        global time_for_not
        time_for_not = int(msg.text)
        message_to_send = (
            f"Вы установили время {str(time_for_not)}:00 для получения уведомлений"
        )
        bot.send_message(msg.chat.id, message_to_send)

    @bot.message_handler(commands=["start_scheduling"])
    def start_scheduling(msg):
        global time_for_not
        while True:
            current_time = datetime.now().time()
            target_time = time(int(time_for_not), 35)
            if (
                current_time.hour == target_time.hour
                and current_time.minute == target_time.minute
            ):
                message_to_send = (
                    f"Сейчас {target_time.hour}:00. Самое время заняться английским!"
                )
                bot.send_message(msg.chat.id, message_to_send)
                sleep(61)

    bot.polling(none_stop=True)
