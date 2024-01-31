from src.actions.const import buttons_available_action_psychologist
from src.answer.answer import ANSWER_BOT
from src.utils.utils import generateReplyMarkup


class BotActions:
    """Действия с ответами бота"""

    def __init__(self, bot, my_db):
        try:
            if not bot or not my_db:
                raise 'Не передан bot или my_db'
            self.bot = bot
            self.my_db = my_db
            print('---INIT BotActions---')
        except Exception as ex:
            print('Ошибка инициализации BotActions', ex)

    def welcomePsychologists(self):
        """Приветствие для психолога"""
        dict_all_psychologists = self.my_db.getAllPsychologists()

        for psychologist_id in dict_all_psychologists:
            reply_markup = generateReplyMarkup(buttons_available_action_psychologist)
            answer = f'{ANSWER_BOT["welcome_psychologist"]}\n{ANSWER_BOT["all_commands_psychologist"]}'

            self.bot.send_message(chat_id=psychologist_id, text=answer, reply_markup=reply_markup)
