import aiohttp

from config import API_URL


async def user_exists(id_tg):
    async with aiohttp.ClientSession() as session:
        params = {
            'tg_id': id_tg
        }
        async with session.get(f'{API_URL}/user/by_id_tg', params=params) as response:
            return response.status == 200


async def add_user(id_tg):
    async with aiohttp.ClientSession() as session:
        params = {
            'id_tg': str(id_tg)
        }
        async with session.post(f'{API_URL}/user', params=params) as response:
            return response.status


async def get_user_info(id_tg) -> dict:
    async with aiohttp.ClientSession() as session:
        params = {
            'tg_id': id_tg
        }
        async with session.get(f'{API_URL}/user/by_id_tg', params=params) as response:
            if response.status == 404:
                add_user_response = await add_user(id_tg)
                if add_user_response:
                    async with session.get(f'{API_URL}/user/by_id_tg', params=params) as response_final:
                        return await response_final.json()
            return await response.json()


def get_clean_user_info(user_info):
    group_id: str = f'group_id: {user_info.get("group_id")}'
    education_id: str = f'education_id: {user_info.get("education_id")}'
    jwt_token: str = f'jwt_token: {"добавлен" if bool(user_info.get("jwt_token")) else "None"}'
    res = '\n'.join((education_id, group_id, jwt_token))
    return res


async def save_user_info(id_tg: int, user_info: dict):
    async with aiohttp.ClientSession() as session:
        params = {'id_tg': id_tg}
        async with session.post(f'{API_URL}/user/update', params=params, json=user_info) as response:
            return response.status


def _abbreviation(marks_res: str):
    return marks_res.replace('Основы безопасности жизнедеятельности', 'ОБЖ')\
        .replace('Изобразительное искусство', 'ИЗО')\
        .replace('Физическая культура', 'Физ-ра')\
        .replace('Иностранный язык (английский)', 'Английский язык')\
        .replace('История России. Всеобщая история', 'История')\
        .replace('Иностранный язык (английский язык)', 'Английский язык')\
        .replace('Алгебра и начала математического анализа', 'Алгебра')\
        .replace('Вероятность и статистика', 'Вер. и статистика')


def _sort_quater(subject_data, subject) -> str:
    average = subject_data['average'][0]
    count = subject_data['count_marks'][0]
    target_grade = '' if not subject_data['target_grade'] else subject_data['target_grade']
    final_m = ''
    if subject_data['final_q']:
        final_m = '=> ' + str(subject_data['final_q'][0])
    last_3 = ' '.join(list(map(str, subject_data['last_three'])))
    result = f'<i>{subject}</i>  {last_3}  ({count})  <i>{average}</i> {final_m} {target_grade}\n'
    return result


def _sort_year(sub_data: dict, subject) -> str:
    finals_q = ' '.join(map(str, sub_data['final_q'][::-1]))
    finals_y = "=> " + str(sub_data['final_years'][0]) if sub_data['final_years'] else ''
    final = "| " + str(sub_data['final'][0]) if sub_data['final'] else ''
    result = f"<i>{subject}</i>  {sub_data['average'][0]} ({sub_data['count_marks'][0]}) {finals_q} {finals_y} {final}\n"
    return result


def sort_marks(data:dict, period_name) -> str:
    result = f'{period_name}\n\n'

    finals_average = data['finals_average_q']
    all_finals_y = data['finals_average_y']

    for subject, subject_data in data.items():
        if subject not in ['finals_average_q', 'finals_average_y']:
            if period_name == 'Год':
                result += _sort_year(subject_data, subject)
            else:
                result += _sort_quater(subject_data, subject)
    if finals_average:
        result += f'\nСр. балл аттестации - {finals_average}'
    if all_finals_y:
        result += f'\nСр. балл итоговой аттестации - {all_finals_y}'
    return _abbreviation(result)


async def get_marks(id_tg: int, period: str):
    async with aiohttp.ClientSession() as session:
        params = {
            'id_tg': id_tg
        }
        async with session.get(f'{API_URL}/marks/get_user_periods', params=params) as response_period:
            data: dict = await response_period.json()
            period_data: dict = data.get('result').get(period)
            period_id, date_from, date_to = period_data['id'], period_data['date_from'], period_data['date_to']
            params = {
                'id_tg': id_tg,
                'date_from': date_from,
                'date_to': date_to,
                'period_id': period_id
            }
            async with session.get(f'{API_URL}/marks', params=params) as response_marks:
                if response_marks and response_marks.status == 200:
                    json = await response_marks.json()
                    marks = json.get('result')
                    if marks:
                        return sort_marks(marks, period)
                    return f'Нет оценок за {period}'
                else:
                    return 'Ошибка...'
