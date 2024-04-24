from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher,FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
botapi = 'токен бота'
bot = Bot(botapi)
dp = Dispatcher(bot,storage=MemoryStorage())

class Start(StatesGroup):
    Itext = State()
    Iurl = State()

@dp.message_handler(commands='chatid')
async def chat(msg: types.Message):
    print(msg.chat.id,msg.from_user.id)

@dp.message_handler(commands='send')
async def inp_text(msg: types.Message,state: FSMContext):
    if msg.from_user.id == 392104225 or 5331252448:
        await Start.Itext.set()
        await msg.answer('введите текст, поставив на месте символов с ссылкой "|"\n /cancel для выхода из ввода')
        async with state.proxy() as data:
            data['msg_text'] = []
    else: await msg.answer("у вас нету доступа")

@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ввод остановлен')

@dp.message_handler(state=Start.Itext)
async def inp_url(msg: types.Message, state: FSMContext):
    if not '|' in msg.text:
        await msg.answer('сообщение должно содержать "|"!')
        await state.finish()
    elif '♨' in msg.text:
        await msg.answer('нельзя использовать ♨, так как он используется ботом!!!')
        await state.finish()
    else:
        spl = [msg.text.split('|')]
        print(spl)
        if len(spl[0]) == 2:
            async with state.proxy() as data:
                data['msg_text'] = spl
                await Start.Iurl.set()
                await msg.answer('введите ссылку')
        else:
            await msg.answer('вы ввели слишком много "|"')
            await state.finish()


@dp.message_handler(state=Start.Iurl)
async def ms(msg: types.Message,state: FSMContext):
    async with state.proxy() as data:
        message_text = data['msg_text']
    print(message_text)
    print(msg.text)
    await state.finish()
    await msg.answer('ниже готовый вид сообщения:')
    inline_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("гайд", callback_data='1'))
    await msg.answer(f'{message_text[0][0]} <a href="{msg.text}">🔥🔥🔥</a>  {message_text[0][1]}',
                     parse_mode=types.ParseMode.HTML, reply_markup=inline_keyboard, disable_web_page_preview=True)
    inline_key = reply_markup= types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("да, отправь",
                                callback_data=f'2♨{message_text[0][0]}♨{message_text[0][1]}♨{msg.text}'))
    await msg.answer('отправить это сообщение в канал?',reply_markup=inline_key)


@dp.callback_query_handler(lambda call: call.data.startswith('2'))
async def send_massage(call: types.CallbackQuery):
    data = call.data.split('♨')[1:]
    inline_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("гайд", callback_data='1'))
    await dp.bot.send_message(-1001803055795,f'{data[0]} <a href="{data[2]}">🔥🔥🔥</a>  {data[1]}',
                     parse_mode=types.ParseMode.HTML, reply_markup=inline_keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: call.data.startswith('1'))
async def url(call: types.CallbackQuery):
    is_sub = await bot.get_chat_member(chat_id=call.message.chat.id, user_id=call.from_user.id)
    if is_sub['status'] == 'left':
        answer_text = 'вам нужно подписаться'
    else:
        answer_text = 'нажмите на 🔥🔥🔥в тексте для получения ссылки'
    await call.answer(answer_text,show_alert=True)

if __name__ == '__main__':
    executor.start_polling(dp)

