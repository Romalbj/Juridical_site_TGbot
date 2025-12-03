from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.filters import CommandStart,  Command
import requests
import ast
from aiogram import F
from aiogram.types import ReplyKeyboardRemove

from keyboards import apply, vacancies_str, vacancies, vacancies_choice_kb

global result
result = None



Bot_token = '7948902296:AAGBln_tdEuGpBTKej3NjhhUzqUMjAFPA8s'

bot = Bot(Bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(text=f'Здравствуйте,  {message.from_user.username}! Используйте /vacancies, чтобы узнать список открытых вакансий, и /book_interview, чтобы записаться на собеседование.')


@dp.message(Command('vacancies'))
async def show_vacancies_command(message: types.Message):
    global result
    # vacancies_str = str(requests.get('http://127.0.0.1:8000/api/jobslist').json()).strip('[').strip(']')
    # vacancies = ast.literal_eval(vacancies_str)


    result = {
        index+1:
            {
                'Должность: ': job['name'].lower(),
                'Город: ': job['city'],
                'Опыт_работы: ': job['experience'].lower()
            }

        for index, job in enumerate(vacancies)
    }

    vacanices_amount = len(result)


    final = []
    for k, v in result.items():
        final.append(str(k))
        content = []
        for keye, value in v.items():
            content.append(f'<b>{keye}</b>')
            content.append(f'{value}\n')
            # content.append('\n')
        # print(content)

        final.append('\n'.join(content))
        final.append('---------------')  # добавляем линию разделителя между вакансиями

    final_str = '\n'.join(final)
    # print(result)
    # print(final)


    await message.answer(text=f'Список доступных вакансий:\n {final_str}',
                         parse_mode='HTML',
                         reply_markup=apply
                    )



@dp.callback_query(F.data.in_(['apply']))
async def application_info(callback: types.CallbackQuery):

    await callback.message.answer(text=f'Выберите вакансию',
                                  reply_markup= await vacancies_choice_kb(),
                                  resize_keyboard=True,
                                  one_time_keyboard=True,
                            )


@dp.callback_query()
async def application(callback: types.CallbackQuery):
    global result
    data = callback.data
    if data and data.startswith('vacancy_'):
        vacancy_number = int(callback.data.split('_')[1])

        job_name = result[vacancy_number]['Должность: ']
        # print('job', job_name)
        # print('result', type(result), result, vacancy_number)

        await callback.message.answer(text=f'Вы выбрали вакансию: {job_name}.\nТеперь заполните информацию для связи.\nУкажите свою эл. почту.')
        # await callback.message.answer(text=f'ясно понятно',)



# @dp.message()
# async def application(message: types.Message):
#     await message.answer(
#         text=f'ну и дурак',
#         reply_markup=ReplyKeyboardRemove()
#     )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
