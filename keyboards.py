from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import requests
import ast
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

vacancies_str = str(requests.get('http://127.0.0.1:8000/api/jobslist').json()).strip('[').strip(']')
vacancies = ast.literal_eval(vacancies_str)
vacancies_amount = len(vacancies)



apply = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Откликнуться на вакансию', callback_data='apply')
    ],
])



async def vacancies_choice_kb():
    builder = InlineKeyboardBuilder()
    for i in range(1, vacancies_amount + 1):
        button = InlineKeyboardButton(
            text=f'{i}',
            callback_data=f'vacancy_{i}'
        )
        builder.add(button)
    return builder.adjust(3).as_markup()