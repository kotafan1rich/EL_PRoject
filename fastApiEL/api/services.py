import random
import datetime

import requests


class Mark:
    current_year = datetime.datetime.now().year
    next_year = current_year + 1
    """Класс для описания словаря оценок.

    Returns:
        dict: <прредмет>: <даннные по предмету>
    """

    # __bad_estimate_value_name = ['замечание', 'неизвестная', 'по болезни', 'зачёт']
    # __bad_estimate_type_name = ['годовая', 'итоговая', 'четверть', 'посещаемость']
    # finals_estimate_type_name = ['годовая', 'итоговая', 'четверть']
    # __good_value_of_estimate_type_name = ['работа', 'задание', 'диктант', 'тест', 'чтение', 'сочинение', 'изложение',
    #                                       'опрос', 'зачёт']

    def __init__(self):
        with open('api/useragents/user_agent.txt', encoding='UTF-8') as f:
            user_agents = f.readlines()
        self.user_agent = random.choice(user_agents).strip()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru,en;q=0.9',
            'Access-Control-Allow-Origin': '*',
            'Connection': 'keep-alive',
            'Content-Type': 'text/plain',
            'Referer': 'https://dnevnik2.petersburgedu.ru/estimate',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-agent': self.user_agent,
            'X-KL-Ajax-Request': 'Ajax_Request',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
        }

    @staticmethod
    def get_target_grade(marks: list[int], average: float):
        if average < 4.5:
            return f'{int((4.5 * len(marks) - sum(marks)) / 0.5)}+'


    # @classmethod
    # def chek_esimate_type_name(cls, estimate_type_name: str):
    #     """Валидность категории записи из эл. дневника
    #
    #     Args:
    #         estimate_type_name (str): категория записи
    #
    #     Returns:
    #         bool: True or False
    #     """
    #     return any(
    #         good_value in estimate_type_name.lower()
    #         for good_value in cls.__good_value_of_estimate_type_name
    #     )

    @staticmethod
    def get_marks_dict(response: list, marks: dict):
        """Получение словаря оценок

        Args:
            response (list): данные после запроса к эл. дневнику
            marks (dict): промежуточно сформированные данные из др. страниц с запроса

        Returns:
            dict: <предмет>: <данные>
        """
        marks_info = response

        for subject_data in marks_info:
            subject_name = subject_data['subject_name']
            estimate_value_name = subject_data['estimate_value_name']

            # if (str(estimate_value_name).lower() not in self.__bad_estimate_value_name) and (
            #         estimate_value_name.lower() not in self.__bad_estimate_type_name) and (
            #         self.chek_esimate_type_name(subject_data['estimate_type_name'])):
            marks[subject_name]['q_marks'].append(int(estimate_value_name))

            # else:
            for estimate_type_name_split in subject_data['estimate_type_name'].split():
                if estimate_type_name_split in ['четверть', ]:
                    marks[subject_name]['final_q'].append(int(estimate_value_name))
                elif estimate_type_name_split in ['Годовая']:
                    marks[subject_name]['final_years'].append(int(estimate_value_name))
                elif estimate_type_name_split in ['Итоговая']:
                    marks[subject_name]['final'].append(int(estimate_value_name))
                elif estimate_type_name_split in ['Экзамен']:
                    marks[subject_name]['exam'].append(int(estimate_value_name))

        return marks

    def get_marks(self, group_id: int, education_id: int, date_from: str, date_to: str, jwt_token: str):
        """Получение словаря с данными по предмету

        Args:
            date_from (str):
            date_to (str):
            group_id (int):
            education_id (int):
            jwt_token (str)

        Returns:
            dict
        """

        params = {
            'p_educations[]': education_id,
            'p_date_from': date_from,
            'p_date_to': date_to,
            'p_limit': '100',
            'p_estimate_types[]': (str(i) for i in [*range(1, 32), 35] if i != 15),
        }

        cookies = {
            '_ga': 'GA1.2.1200595638.1657698485',
            '_ym_uid': '1657698485160238417',
            '5c5cf8878acb5060ca4c77c2': '[41,39,36,31,26,24]',
            'sessionHiddenMessages': '[19]',
            '__utmc': '263703443',
            '_ym_d': '1693172101',
            '_gid': 'GA1.2.1531138517.1696012332',
            '_ym_isad': '2',
            '__utma': '263703443.1200595638.1657698485.1696013152.1696019883.7',
            '__utmz': '263703443.1696019883.7.7.utmcsr=dnevnik2.petersburgedu.ru|utmccn=(referral)|utmcmd=referral|utmcct=/',
            'X-JWT-Token': jwt_token,
        }

        response = requests.get('https://dnevnik2.petersburgedu.ru/api/journal/estimate/table', cookies=cookies, params=params, headers=self.headers, timeout=10).json().get('data').get('items')

        sort_response = sorted(response, key=lambda x: datetime.datetime.strptime(x['date'], '%d.%m.%Y'))

        params_list_subjects = {
            # 'p_limit': '100'
            # 'p_page': '1',
            'p_educations[]': education_id,
            'p_groups[]': group_id,

        }
        list_subjects = requests.get('https://dnevnik2.petersburgedu.ru/api/journal/subject/list-studied',
                                     cookies=cookies,
                                     params=params_list_subjects, headers=self.headers,
                                     timeout=10).json().get('data').get('items')

        marks = {
            info_marks_all['name']: {
                'q_marks': [],
                'last_three': [],
                'count_marks': [],
                'average': [],
                'target_grade': None,
                'final_q': [],
                'final_years': [],
                'final': [],
                'exam': []
            }
            for info_marks_all in list_subjects
        }
        marks = self.get_marks_dict(response=sort_response, marks=marks)

        for sub in marks.copy():
            try:
                sub_info = marks[sub]

                last_three: list = sub_info['q_marks'][-3::]
                sub_info['last_three'] = last_three

                sub_info['final_q'].reverse()

                count_marks = len(sub_info['q_marks'])
                sub_info['count_marks'].append(count_marks)

                sum_marks = sum(sub_info['q_marks'])
                average = round(sum_marks / count_marks, 2)
                sub_info['average'].append(average)

                sub_info['target_grade'] = self.get_target_grade(sub_info['q_marks'], average)

                # del sub_info['q_marks']
            except ZeroDivisionError:
                del marks[sub]
        return marks

    def sort_marks(self, data: dict, date_from: str, date_to: str):
        """Сортировка словаря

        Args:
            data (dict): данные по предметам
            date_from (str)
            date_to (str)

        Returns:
            dict: отсортированный
        """
        sort_result = dict(sorted(data.items()))
        res = sort_result | self._sort_finals_quater(sort_result) if not (date_from == f'1.09.{self.current_year}' and date_to == f'31.05.{self.next_year}') else sort_result | self._sort_finals_year(sort_result)

        return res

    @staticmethod
    def _sort_finals_quater(data):
        all_finals = [marks_info['final_q'][0] for marks_info in data.values() if bool(marks_info['final_q'])]
        return {'finals_average_q': round(sum(all_finals) / len(all_finals), 2) if all_finals else None}

    @staticmethod
    def _sort_finals_year(sort_result):
        all_finals_q = [i['final_years'][0] for i in sort_result.values() if i['final_years']]
        all_finals_y = [i['final'][0] for i in sort_result.values() if i['final']]

        return {'finals_average_q': round(sum(all_finals_q) / len(all_finals_q), 2) if all_finals_q else None,
                'finals_average_y': round(sum(all_finals_y) / len(all_finals_y), 2) if all_finals_y else None}

