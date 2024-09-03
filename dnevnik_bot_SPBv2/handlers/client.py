from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from create_bot import bot
from keyboards import kb_client_settings, education_id_b, group_id_b, settings_b, \
    change_info_b, kb_client_set_params, save_b, cancel_b, get_kb_client_main, help_b, change_jwt_b
from messages import HELP, SETTINGS, ERROR_MES, CHANGE_JWT, ADDED, CANCELED, CHANGE_SETTINGS, NOT_ADDED_SETTINGS

from .other import user_exists, add_user, get_user_info, get_clean_user_info, save_user_info, get_marks

admins = (1324716819,)

PERIOD_TEXTS = ['1 четверть', '2 четверть', '3 четверть', '4 четверть', 'I полугодие', 'II полугодие', 'Год']


class FSMSettings(StatesGroup):
    user_info = State()
    change_info = State()
    education_id = State()
    group_id = State()
    jwt_token = State()


async def start(message: types.Message):
    id_tg = message.from_user.id
    if not await user_exists(id_tg) and await add_user(id_tg):
        await bot.send_message(id_tg, f'Здравствуйте\n\n{HELP}', reply_markup=await get_kb_client_main(id_tg))
    else:
        await bot.send_message(id_tg, HELP, reply_markup=await get_kb_client_main(id_tg), parse_mode=None)


async def get_settings(message: types.Message, state: FSMContext):
    user_info = await get_user_info(message.from_user.id)
    clean_user_info: str = get_clean_user_info(user_info)

    await state.set_state(FSMSettings.user_info)
    await bot.send_message(message.from_user.id, f'{SETTINGS}\n{clean_user_info}', reply_markup=kb_client_settings)


async def change_info(message: types.Message, state: FSMContext):
    await state.set_state(FSMSettings.change_info)
    await bot.send_message(message.from_user.id,
                           CHANGE_SETTINGS,
                           reply_markup=kb_client_set_params)


async def set_settings(message: types.Message, state: FSMContext):
    param = message.text
    id_tg = message.from_user.id

    if param == save_b.text:
        params = await state.get_data()
        res = await save_user_info(id_tg=message.from_user.id, user_info=params)
        text = ADDED if res else ERROR_MES
        await bot.send_message(message.from_user.id, text,
                               reply_markup=await get_kb_client_main(id_tg))
        await state.clear()

    else:
        if param == education_id_b.text:
            await state.set_state(FSMSettings.education_id)
        elif param == group_id_b.text:
            await state.set_state(FSMSettings.group_id)
        elif param == change_jwt_b.text:
            await state.set_state(FSMSettings.jwt_token)
        else:
            return await state.clear()
        await bot.send_message(message.from_user.id,
                               f'Введите {param}',
                               reply_markup=kb_client_set_params)


async def set_education_id(message: types.Message, state: FSMContext):
    await state.update_data(education_id=int(message.text))
    await state.set_state(FSMSettings.change_info)
    await bot.send_message(message.from_user.id, 'Установленно, не забудьте сохранить',
                           reply_markup=kb_client_set_params)


async def set_group_id(message: types.Message, state: FSMContext):
    await state.update_data(group_id=int(message.text))
    await state.set_state(FSMSettings.change_info)
    await bot.send_message(message.from_user.id, 'Установленно, не забудьте сохранить',
                           reply_markup=kb_client_set_params)


async def set_jwt(message: types.Message, state: FSMContext):
    await state.update_data(jwt_token=message.text)
    await state.set_state(FSMSettings.change_info)
    await bot.send_message(message.from_user.id, 'Установленно, не забудьте сохранить',
                           reply_markup=kb_client_set_params)


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    current_state = await state.get_state()
    if current_state is None:
        pass
    else:
        await state.clear()
    await message.answer(
        CANCELED,
        reply_markup=await get_kb_client_main(user_id),
    )


async def get_marks_handler(message: types.Message):
    id_tg = message.from_user.id
    period = message.text
    marks = await get_marks(id_tg=id_tg, period=period)
    await bot.send_message(message.from_user.id, marks, reply_markup=await get_kb_client_main(id_tg))


async def change_jwt(message: types.Message, state: FSMContext):
    await state.set_state(FSMSettings.jwt_token)
    await bot.send_message(message.from_user.id, CHANGE_JWT)


async def help(message: types.Message):
    id_tg = message.from_user.id

    await bot.send_message(message.from_user.id, HELP, reply_markup=await get_kb_client_main(id_tg), parse_mode=None)


def register_handlers_client(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    dp.message.register(cancel_handler, F.text == cancel_b.text)
    dp.message.register(get_settings, F.text == settings_b.text)
    dp.message.register(change_info, F.text == change_info_b.text)
    dp.message.register(set_settings, F.text.in_((education_id_b.text, group_id_b.text, change_jwt_b.text, save_b.text)))
    dp.message.register(set_education_id, FSMSettings.education_id)
    dp.message.register(set_group_id, FSMSettings.group_id)
    dp.message.register(set_jwt, FSMSettings.jwt_token)
    dp.message.register(get_marks_handler, F.text.in_(PERIOD_TEXTS))
    dp.message.register(change_jwt, F.text == change_jwt_b.text)
    dp.message.register(help, F.text == help_b.text)
