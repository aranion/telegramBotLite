from src.actions.const import buttons_available_action_psychologist
from src.answer.answer import ANSWER_BOT
from src.commands.const import COMMANDS, PRIVATE_COMMANDS
from src.commands.enums import ListCommands, ListPrivateCommands
from src.utils.utils import generateReplyMarkup, getValueEnum


def commandInit(bot, my_db):
    @bot.message_handler(commands=[getValueEnum('START', ListCommands)])
    def _start(message):
        chat_id = message.chat.id
        answer = ''
        reply_markup = None

        if message.chat.type == 'private':
            my_db.addNewChat(message.chat)

        is_psychologist = my_db.checkIsPsychologist(chat_id)

        if is_psychologist:
            answer = ANSWER_BOT['all_commands_psychologist']
            reply_markup = generateReplyMarkup(buttons_available_action_psychologist)
            bot.send_message(chat_id=chat_id, text=answer, reply_markup=reply_markup)
        else:
            bot.send_message(chat_id, ANSWER_BOT['start'], parse_mode='html')

    @bot.message_handler(commands=[getValueEnum('INFO', ListCommands)])
    def _info(message):
        chat_id = message.chat.id

        bot.send_message(chat_id, ANSWER_BOT['about_bot'])

    @bot.message_handler(commands=[getValueEnum('HELP', ListCommands)])
    def _help(message):
        chat_id = message.chat.id
        commands = '\n'
        is_psychologist = my_db.checkIsPsychologist(chat_id)

        for command in COMMANDS:
            commands += f"/{''.join(command['command'])} - {command['description']}\n"

        if is_psychologist:
            commands += f"\nКак психологу вам доступны дополнительные команды:\n"
            for command in PRIVATE_COMMANDS:
                commands += f"/{''.join(command['command'])} - {command['description']}\n"

        bot.send_message(chat_id, 'Команды: ' + commands, parse_mode='html')

    @bot.message_handler(commands=[getValueEnum('GET_ALL_COMMANDS_PSYCHOLOGISTS', ListPrivateCommands)])
    def _get_all_commands_psychologist(message):
        chat_id = message.chat.id

        is_psychologist = my_db.checkIsPsychologist(chat_id)

        if not is_psychologist:
            return

        reply_markup = generateReplyMarkup(buttons_available_action_psychologist)
        bot.send_message(chat_id, ANSWER_BOT['all_commands_psychologist'], reply_markup=reply_markup)
