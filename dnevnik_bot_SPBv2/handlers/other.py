import datetime

import aiohttp

from config import API_HOST, API_PORT, API_URL

current_year = datetime.datetime.now().year
next_year = current_year + 1

dates = {
    1: (f'1.09.{current_year}', f'26.10.{current_year}'),
    2: (f'5.11.{current_year}', f'28.12.{current_year}'),
    3: (f'09.01.{next_year}', f'23.03.{next_year}'),
    4: (f'03.04.{next_year}', f'31.05.{next_year}')
}


async def user_exists(id_tg):
    async with aiohttp.ClientSession() as session:
        json = {
            'tg_id': id_tg
        }
        async with session.get(f'{API_URL}/user/by_id_tg', json=json) as response:
            return response.status == 200


async def add_user(id_tg):
    async with aiohttp.ClientSession() as session:
        json = {
            'tg_id': id_tg
        }
        async with session.post(f'{API_URL}/user', json=json) as response:
            return response.status == 200


async def get_user_info(id_tg):
    async with aiohttp.ClientSession() as session:
        json = {
            'tg_id': id_tg
        }
        async with session.get(f'{API_URL}/user/by_id_tg', json=json) as response:
            if response.status == 404:
                add_user_response = await add_user(id_tg)
                if add_user_response:
                    async with session.get(f'{API_URL}/user/by_id_tg', json=json) as response_finall:
                        return await response_finall.json()
            return await response.json()


def get_clean_user_info(user_info):
    group_id: str = f'Ваш group_id: {user_info.get("group_id")}'
    education_id: str = f'Ваш education_id: {user_info.get("education_id")}'
    res = '\n'.join((education_id, group_id))
    return res


async def save_user_info(id_tg: int, user_info: dict):
    async with aiohttp.ClientSession() as session:
        json = user_info | {'id_tg': id_tg}
        async with session.get(f'{API_URL}/user/update', json=json) as response:
            return response.status


def _abbreviation(marks_res: str):
    return (
        marks_res.replace('Основы безопасности жизнедеятельности', 'ОБЖ')
        .replace('Изобразительное искусство', 'ИЗО')
        .replace('Физическая культура', 'Физ-ра')
        .replace('Иностранный язык (английский)', 'Английский язык')
        .replace('История России. Всеобщая история', 'История')
        .replace('Иностранный язык (английский язык)', 'Английский язык')
        .replace('Алгебра и начала математического анализа', 'Алгебра')
    )


def _sort_quater(data, sort_result, name_period):
    finals_average = data['finals_average_q']
    result = f'{name_period}\n\n'
    for subject, subject_data in sort_result.items():
        if subject != 'finals_average_q':
            average = subject_data['average'][0]
            count = subject_data['count_marks'][0]
            final_m = ''
            if subject_data['final_q']:
                final_m = '=> ' + str(subject_data['final_q'][0])
            last_3 = ' '.join(list(map(str, subject_data['last_three'])))
            result += f'<i>{subject}</i>  {last_3}  ({count})  <i>{average}</i> {final_m}\n'
    if finals_average:
        result += f'\nСр. балл аттестации - {finals_average}'
    return _abbreviation(result)


def _sort_year(sort_result, name_period):
    result = f'{name_period}\n\n'
    all_finals_q = sort_result['finals_average_q']
    all_finals_y = sort_result['finals_average_y']
    for subject, sub_data in sort_result.items():
        if subject not in ['finals_average_q', 'finals_average_y']:
            finals_q = ' '.join(map(str, sub_data['final_q'][::-1]))
            finals_y = "=> " + str(sub_data['final_years'][0]) if sub_data['final_years'] else ''
            final = "| " + str(sub_data['final'][0]) if sub_data['final'] else ''
            result += f"<i>{subject}</i>  {sub_data['average'][0]} ({sub_data['count_marks'][0]}) {finals_q} {finals_y} {final}\n"
    if all_finals_q:
        result += f'\nСр. балл годовой аттестации - {all_finals_q}'
    if all_finals_y:
        result += f'\nСр. балл итоговой аттестации - {all_finals_y}'
    return _abbreviation(result)


async def get_marks_quater(id_tg: int, quater: int):
    date_from, date_to = dates[quater]
    async with aiohttp.ClientSession() as session:
        json_data = {
            'id_tg': id_tg,
            'date_from': date_from,
            'date_to': date_to
        }
        async with session.get(f'{API_URL}/marks', json=json_data) as response:
            if response:
                json = await response.json()
                marks = json.get('result')
                if marks:
                    return _sort_quater(marks, marks, f'{quater} четверть') if response.status == 200 else 'Ошибка...'
            return f'Нет оценок за {quater}-ую четверть'


async def get_marks_half(id_tg: int, half: int):
    if half == 1:
        date_from = dates[1][0]
        date_to = dates[2][1]
    else:
        date_from = dates[3][0]
        date_to = dates[4][1]
    async with aiohttp.ClientSession() as session:
        json_data = {
            'id_tg': id_tg,
            'date_from': date_from,
            'date_to': date_to
        }
        async with session.get(f'{API_URL}/marks', json=json_data) as response:
            json = await response.json()
            marks = json.get('result')
            if marks:
                return _sort_quater(marks, marks, f'{half} полугодие') if response.status == 200 else 'Ошибка...'
            return f'Нет оценок за {half}-ое полугодие'


async def get_marks_year(id_tg: int):
    date_from = dates[1][0]
    date_to = dates[4][1]
    async with aiohttp.ClientSession() as session:
        json_data = {
            'id_tg': id_tg,
            'date_from': date_from,
            'date_to': date_to
        }
        async with session.get(f'{API_URL}/marks', json=json_data) as response:
            json = await response.json()
            marks = json.get('result')
            if marks:
                return _sort_year(marks, f'Год') if response.status == 200 else 'Ошибка...'
            return f'Нет оценок за год'

