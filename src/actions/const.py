from src.utils.utils import getValueEnum

ALL_BUTTONS = {
    'ALL_MESSAGE': {
        'text': '📬 Получить все сообщения',
        'action': getValueEnum('GET_ALL_MESSAGES')
    }
}

# Доступные действия для психологов:
buttons_available_action_psychologist = [
    ALL_BUTTONS['ALL_MESSAGE']
]
# Доступные действия для пользователя
buttons_available_action_user = []
