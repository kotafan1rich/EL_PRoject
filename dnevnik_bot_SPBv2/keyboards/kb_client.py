from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

quater_1_b = KeyboardButton(text='1 четверть')
quater_2_b = KeyboardButton(text='2 четверть')
quater_3_b = KeyboardButton(text='3 четверть')
quater_4_b = KeyboardButton(text='4 четверть')
half_1_b = KeyboardButton(text='1 полугодие')
half_2_b = KeyboardButton(text='2 полугодие')
year_b = KeyboardButton(text='Год')
help_b = KeyboardButton(text='Помощь')
settings_b = KeyboardButton(text='Настройки')
cancel_b = KeyboardButton(text='Отмена')
change_info_b = KeyboardButton(text='Изменить информацию')
education_id_b = KeyboardButton(text='education_id')
group_id_b = KeyboardButton(text='group_id')
group_name_b = KeyboardButton(text='group_name')
save_b = KeyboardButton(text='Сохранить')
change_jwt_b = KeyboardButton(text='Изменить jwt')

kb_client_main_bottoms = [
    [quater_1_b, quater_2_b, quater_3_b, quater_4_b],
    [half_1_b, half_2_b],
    [year_b],
    [settings_b, help_b]
]

# kb_client_main_text_bottoms = [*ilist(map(lambda x: [i.text for i in x], kb_client_main_bottoms))]

kb_client_settings_bottms = [
    [change_info_b, change_jwt_b],
    [cancel_b]
]

kb_client_set_params_bottms = [
    [education_id_b, group_id_b, group_name_b],
    [save_b],
    [cancel_b]
]


kb_client_main = ReplyKeyboardMarkup(keyboard=kb_client_main_bottoms, resize_keyboard=True)
kb_client_settings = ReplyKeyboardMarkup(keyboard=kb_client_settings_bottms, resize_keyboard=True)
kb_client_set_params = ReplyKeyboardMarkup(keyboard=kb_client_set_params_bottms, resize_keyboard=True)
