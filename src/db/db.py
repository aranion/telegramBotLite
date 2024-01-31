import firebase_admin
from firebase_admin import credentials, db
from src.answer.answer import ANSWER_BOT


class MyDB:
    """Управление БД"""

    def __init__(self, config):
        try:
            if not config:
                raise ValueError('Не передан config')
            self.cred = credentials.Certificate(config['serviceAccount'])
            firebase_admin.initialize_app(self.cred, {'databaseURL': config['firebase']['databaseURL']})
            print('---INIT DB---')
        except ValueError as ex:
            print('Ошибка инициализации database', ex)

    @staticmethod
    def setLogs(err):
        try:
            print('MyDB->setLogs')

            ref_main = db.reference('/logs/')
            ref_main.push(f"Ошибка: {''.join(err.args)}")
        except Exception as ex:
            print('Ошибка при записи лога', ex)

    @staticmethod
    def addNewChat(chat):
        """Добавить новый чат, если он еще не добавлен"""
        try:
            print('MyDB->addNewChat')

            chat_id = chat.id
            ref_chats = db.reference('/chats/')
            data = ref_chats.get()

            if (not data) or (not data.get(str(chat_id))):
                ref_new_data = ref_chats.child(f'{chat_id}')
                # Пользователи с расширенными правами
                super_psychologists = ['854241396', '748249007']
                is_super_user = str(chat_id) in super_psychologists

                ref_new_data.set({
                    'username': chat.username,
                    'first_name': chat.first_name,
                    'last_name': chat.last_name,
                    'type': chat.type,
                    'id': chat_id,
                    'is_psychologist': is_super_user,
                    'is_super_user': is_super_user
                })
                return
        except Exception as ex:
            print('Ошибка при добавлении нового чата', ex)

    @staticmethod
    def getAllPsychologists():
        """Получить всех психологов"""
        try:
            print('MyDB->getAllPsychologists')

            ref_chats = db.reference('/chats/')
            data = ref_chats.get()
            dict_all_psychologists = {}

            if not data:
                return dict_all_psychologists
            for chat_id in data:
                is_psychologist = data[chat_id].get('is_psychologist')
                if is_psychologist:
                    dict_all_psychologists[chat_id] = data[chat_id]
            return dict_all_psychologists
        except Exception as ex:
            print('Ошибка при получении всех психологов', ex)

    @classmethod
    def getAllMessages(cls, current_chat_id):
        """Получить все сообщения для психолога"""
        try:
            print('MyDB->getAllMessages')

            is_psychologist = cls.checkIsPsychologist(current_chat_id)

            if not is_psychologist:
                return ANSWER_BOT['not_access']

            ref_messages_psychologist = db.reference('/messages/')
            ref_chats = db.reference('/chats/')
            data = ref_messages_psychologist.get()
            data_chats = ref_chats.get()
            result = []

            for key in data:
                item = data[key]
                item['chat'] = data_chats[f'{item.get("chat_id")}']
                result.append(item)

            return result
        except Exception as ex:
            print('Ошибка при получении всех сообщений психологу', ex)

    @staticmethod
    def checkIsPsychologist(chat_id):
        """Проверить есть ли у пользователя права психолога"""
        try:
            print('MyDB->checkIsPsychologist')

            ref_chat = db.reference(f'/chats/{chat_id}/')
            data = ref_chat.get()

            if data:
                return data.get('is_psychologist')
            return False
        except Exception as ex:
            print('Ошибка при проверки на права психолога', ex)

    @classmethod
    def setMessage(cls, message):
        """Записать все произвольные сообщения пользователя(кроме сообщения психолога)"""
        try:
            print('MyDB->setMessage')
            chat_id = message.chat.id
            is_psychologist = cls.checkIsPsychologist(chat_id)

            # Если это сообщение психолога, то добавлять его в DB не нужно
            if is_psychologist:
                return

            ref_messages = db.reference('/messages/')
            new_message = {'chat_id': chat_id, 'date': message.date, 'message_id': message.message_id,
                           'text': message.text}

            ref_messages.push(new_message)
        except Exception as ex:
            print('Ошибка при записи сообщения в БД', ex)
