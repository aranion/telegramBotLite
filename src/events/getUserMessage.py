from src.answer.answer import ANSWER_BOT


def eventGetUserMessageInit(bot, my_db, catch):
    @bot.message_handler(content_types=['text'])
    def get_user_text(message):
        try:
            chat_id = message.chat.id
            is_psychologist = my_db.checkIsPsychologist(chat_id)

            # Если сообщение отправляет психолог
            if is_psychologist:
                # Психолог не может отправлять себе сообщения
                bot.send_message(chat_id, ANSWER_BOT['psychologist_not_sent_message'], parse_mode='html')
            else:
                # Записываются все сообщения от пользователя
                my_db.setMessage(message)

                # Получаем всех психологов
                all_psychologists = my_db.getAllPsychologists()
                # Формируем сообщение для психолога
                new_user_message = f'{ANSWER_BOT["new_message_received"]}:\n' \
                                   f'{ANSWER_BOT["item_message"].format(message.message_id, message.chat.username, message.chat.first_name, message.text)}'

                # Отправить поступившее сообщение с вопросом в чаты психологов
                for psychologist in all_psychologists:
                    bot.send_message(psychologist, new_user_message, parse_mode='html')
                # Уведомить пользователя об успешной отправки сообщения
                bot.reply_to(message, ANSWER_BOT['successfully_sent'])
        except Exception as ex:
            catch(ex)

    @bot.message_handler()
    # @bot.message_handler(content_types=['photo', 'audio', 'sticker', 'document', 'video', 'video_note', 'voice', 'location', 'contact', ''])
    def get_user_other(message):
        bot.send_message(message.chat.id, ANSWER_BOT['i_dont_know_format_file'])
