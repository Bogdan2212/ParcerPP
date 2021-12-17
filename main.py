from aiogram import types ,Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup, ReplyKeyboardRemove,ReplyKeyboardMarkup
from cSian import cian_parcer
from config import token
from avito_parser import avito_parcer
import asyncio

bot=Bot(token=token)
dp=Dispatcher(bot=bot,storage=MemoryStorage())
bd={}
#keyboard

inline_flat_btn=InlineKeyboardButton('Недвижимость',callback_data='flatButton')
inline_others_btn=InlineKeyboardButton('Другое',callback_data='othersButton')

inline_keyboard=InlineKeyboardMarkup()
inline_keyboard.add(inline_flat_btn)
inline_keyboard.add(inline_others_btn)

keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
cancel_btn='Отмена'
start_btn='/parser'
help_btn='/help'
mail_btn='/mail'
keyboard.add(start_btn)
keyboard.add(help_btn)
keyboard.add(mail_btn)
keyboard_stop=ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_btn)


class Form(StatesGroup):
    mail=State()
    parser=State()

#Добавить состояния на каждый вариант парсинга
class Flats(StatesGroup):
    cian=State()
    cancel=State()
class Others(StatesGroup):
    avito=State()
    cancel=State()
@dp.message_handler(commands=['start'])
async def start_message_command(msg= types.Message,state=FSMContext):
    user_id=msg.from_user.id
    await state.finish()
    await bot.send_message(user_id,'Привет, я бот, который будет сообщать тебе о новых объявлениях!\n')
    if user_id not in bd:
        await bot.send_message(user_id,"Пришлите свою почту, для получения новых уведомлений",reply_markup=ReplyKeyboardRemove())
    await Form.mail.set()

@dp.message_handler(state=Form.mail)
async def get_mail_command(msg=types.Message,state=FSMContext):
    mail=msg.text
    bd[msg.from_user.id]=mail
    await state.finish()
    await bot.send_message(msg.from_user.id,'Ваш email успешно сохранен',reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def help_message_command(msg: types.Message):
    await bot.send_message(msg.from_user.id,'Вот все, что вам нужно:\n/start : Начать работу с ботом\n/help : Вся информация о боте\n/mail имя почты : смена почтового адреса\n/parser : Начать поиск информации\n/stop : Отмена поиска',reply_markup=keyboard)

@dp.message_handler(commands=['mail'])
async def set_mail_command(msg=types.Message):
    bd[msg.from_user.id]=msg.get_args()
    await bot.send_message(msg.from_user.id,f'Ваша Новая почта: {bd[msg.from_user.id]}',reply_markup=keyboard)

@dp.message_handler(commands='parser')
async def start_parsing_command(msg=types.Message):
    await msg.reply('Выберите категорию поиска',reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data=='flatButton')
async def callback_flat_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Введите ссылку на Авито",reply_markup=keyboard_stop)
    await Flats.cian.set()
@dp.message_handler(state=Flats.cian)
async def get_avito_url(msg=types.Message,state=FSMContext):
    request=msg.text
    if request != '/stop' and request != 'Отмена':
        await bot.send_message(msg.from_user.id, 'Для подтверждения Введите длительность в часах\nДля отмены нажмите на кнопку',
                               reply_markup=keyboard_stop)
        await state.update_data(avito_url=request)
        await Flats.next()
    else:
        await bot.send_message(msg.from_user.id, 'Действие отменено', reply_markup=keyboard)
        await state.finish()


@dp.message_handler(state=Flats.cancel)
async def run_cancel_parser(msg=types.Message,state=FSMContext):
    if msg.text=='Отмена':
        await bot.send_message(msg.from_user.id, 'Действие отменено', reply_markup=keyboard)
        await state.finish()
    else:
        user_data= await state.get_data()
        await bot.send_message(msg.from_user.id,f"Вы будете получать уведомления в течении {msg.text} часов",reply_markup=keyboard)
        await state.finish()
        await avito_parcer(user_data['avito_url'], msg.from_user.id, bd[msg.from_user.id],int(msg.text))







@dp.callback_query_handler(lambda c: c.data=='othersButton')
async def callback_others_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Введите ссылку на авито",reply_markup=keyboard_stop)
    await Others.avito.set()
@dp.message_handler(state=Others.avito)
async def others_parsing(msg = types.Message,state= FSMContext):
    request=msg.text
    if request != '/stop' and request != 'Отмена':
        await bot.send_message(msg.from_user.id,f'Для подтверждения Введите длительность в часах\nДля отмены нажмите на кнопку')
        await state.update_data(avito_url=request)
        await Others.next()
    else:
        await bot.send_message(msg.from_user.id,'Действие отменено',reply_markup=keyboard)
        await state.finish()
@dp.message_handler(state=Others.cancel)
async def run_cancel_parser(msg=types.Message,state=FSMContext):
    if msg.text=='Отмена':
        await bot.send_message(msg.from_user.id, 'Действие отменено', reply_markup=keyboard)
        await state.finish()
    else:
        user_data= await state.get_data()
        await bot.send_message(msg.from_user.id,f"Вы будете получать уведомления в течении {msg.text} часов",reply_markup=keyboard)
        await state.finish()
        await avito_parcer(user_data['avito_url'], msg.from_user.id, bd[msg.from_user.id],int(msg.text))
@dp.message_handler(commands='send')
async def command_send_all(msg=types.Message):
    for i in bd:
        await bot.send_message(i,msg.get_args())

@dp.message_handler()
async def others_messages(msg=types.Message):
    await bot.send_message(msg.from_user.id,"Неопознанный объект")





if __name__=='__main__':
    executor.start_polling(dp)
