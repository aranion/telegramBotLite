from src.answer.answer import ANSWER_BOT
from src.utils.utils import generateReplyMarkup, getValueEnum, getAnswerUserData


def actionsInit(bot, my_db, sendResult):
    """Регистрация действий при нажатии кнопок"""

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            # Если сообщение из чата с ботом
            if call.message:
                type_action = call.data
                chat_id = call.message.chat.id

                if type_action == getValueEnum('GET_ALL_MESSAGES'):
                    # Кнопка "Получить все сообщения"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    all_messages = my_db.getAllMessages(chat_id)

                    bot.send_message(chat_id, ANSWER_BOT['all_unallocated_message'], parse_mode='html')

                    if all_messages:
                        i = 0
                        answer = ''

                        for item in all_messages:
                            chat = item.get('chat')
                            message_id = item.get('message_id')
                            text = item.get("text")
                            username = chat.get('username')
                            first_name = chat.get('first_name')
                            answer += ANSWER_BOT['item_message'].format(message_id, username, first_name, text) + '\n\n'
                            i += 1

                            if i == 10:
                                bot.send_message(chat_id, answer, parse_mode='html')
                                answer = ''

                        return bot.send_message(chat_id, answer, parse_mode='html')
                    else:
                        return bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                else:
                    bot.send_message(chat_id, ANSWER_BOT['i_dont_know_actions'])
            elif call.inline_message_id:
                # Если сообщение из инлайн-режима
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=ANSWER_BOT['actions_i_dont_know'])
        except Exception as ex:
            print('Ошибка при выполнении действия', ex)
            bot.send_message(call.message.chat.id, ANSWER_BOT['error'], parse_mode='html')
