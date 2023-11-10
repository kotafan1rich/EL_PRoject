from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from create_bot import bot
from keyboards import kb_client_main, kb_client_settings, education_id_b, group_id_b, settings_b, \
    change_info_b, kb_client_set_params, save_b, cancel_b, quater_4_b, quater_3_b, \
    quater_2_b, quater_1_b, half_2_b, half_1_b, year_b, help_b, change_jwt_b
from messages import HELP, SETTINGS, ERROR_MES, CHANGE_JWT, ADDED, CANCELED, CHANGE_SETTINGS, NOT_ADDED_SETTINGS

from .other import user_exists, add_user, get_user_info, get_clean_user_info, save_user_info, get_marks_quater, \
    get_marks_half, get_marks_year

admins = (1324716819,)


class FSMSettings(StatesGroup):
    user_info = State()
    change_info = State()
    education_id = State()
    group_id = State()
    jwt_token = State()

async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        pass
    else:
        await state.clear()
    await message.answer(
        CANCELED,
        reply_markup=kb_client_main,
    )


async def get_marks_quater_handler(message: types.Message):
    id_tg = message.from_user.id
    text = message.text
    quater = int(text.split()[0])
    user_info = await get_user_info(id_tg)
    if all(user_info.values()):
        marks = await get_marks_quater(id_tg, quater)
        await bot.send_message(id_tg, marks, reply_markup=kb_client_main)
    else:
        await bot.send_message(id_tg, NOT_ADDED_SETTINGS, reply_markup=kb_client_main)


async def get_marks_half_handler(message: types.Message):
    text = message.text
    half: int = int(text.split()[0])
    marks = await get_marks_half(message.from_user.id, half)
    await bot.send_message(message.from_user.id, marks, reply_markup=kb_client_main)


async def get_marks_year_handler(message: types.Message):
    marks = await get_marks_year(message.from_user.id)
    await bot.send_message(message.from_user.id, marks, reply_markup=kb_client_main)


async def change_jwt(message: types.Message, state: FSMContext):
    await state.set_state(FSMSettings.jwt_token)
    await bot.send_message(message.from_user.id, CHANGE_JWT)


async def help(message: types.Message):
    await bot.send_message(message.from_user.id, HELP, reply_markup=kb_client_main, parse_mode=None)


def register_handlers_client(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    dp.message.register(cancel_handler, F.text == cancel_b.text)
    dp.message.register(get_settings, F.text == settings_b.text)
    dp.message.register(change_info, F.text == change_info_b.text)
    dp.message.register(set_settings, F.text.in_((education_id_b.text, group_id_b.text, change_jwt_b.text, save_b.text)))
    dp.message.register(set_education_id, FSMSettings.education_id)
    dp.message.register(set_group_id, FSMSettings.group_id)
    dp.message.register(set_jwt, FSMSettings.jwt_token)
    dp.message.register(get_marks_quater_handler, F.text.in_((quater_1_b.text, quater_2_b.text, quater_3_b.text, quater_4_b.text)))
    dp.message.register(get_marks_half_handler, F.text.in_((half_1_b.text, half_2_b.text)))
    dp.message.register(get_marks_year_handler, F.text == year_b.text)
    dp.message.register(change_jwt, F.text == change_jwt_b.text)
    dp.message.register(help, F.text == help_b.text)
