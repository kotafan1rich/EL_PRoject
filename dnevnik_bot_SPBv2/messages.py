HELP = '''
Для получения ваших оценок требуется узнать ваш уникальный id, с помощью которого можно получить ваши оценки
Для этого перейдите по ссылке офицального сайта Петербуржского образования и отправте боту этот id.

https://dnevnik2.petersburgedu.ru/api/journal/person/related-child-list

Он выглядит примерно так:

{"data":{"items":[{"educations":[{"push_subscribe":true, "education_id": ВАШ ID, ...}

Намите Настройки -> Изменить информацию -> education_id -> ВАШ ID -> Сохранить

Если нужна помощь пишите @Gohdot 

'''

SETTINGS = '''
Ты можешь:
- Изменить education_id
- Изменить group_id
'''

ERROR_MES = 'Ошибка... Оценки не найдены, попробуй ещё раз.'

ADDED = 'Добавлено'

CHANGE_JWT = 'Отправьте jwt'
