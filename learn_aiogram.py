from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
import asyncio

API_TOKEN = '5717773148:AAGBWeWF7aijwkJCrVdC7V1daEF5I351HME'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

PHOTO_WITH_CAT = open('media_files/cute_cat.jpeg', 'rb')
KITTENS = [
    open('media_files/cat_1.jpeg', 'rb'),
    open('media_files/cute_cat.jpeg', 'rb'),
    open('media_files/dog.jpeg', 'rb'),
]
VOICE = open('media_files/myaukane_koshki_-_myaukane_koshki.mp3', 'rb'), 
VIDEO = open('media_files/pexels-anna-tarazevich-5764223.mp4', 'rb')
TEXT_FILE = open('media_files/index.jpeg', 'rb')
VIDEO_NOTE = open('media_files/video_note.mp4', 'rb')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Привет!\nИспользуй /help, '
                        'чтобы узнать список доступных команд!')

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/voice', '/photo', '/group', '/note', '/file', '/testpre', sep='\n')
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands='voice')
async def voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, VOICE,  reply_to_message_id=message.message_id)

@dp.message_handler(commands='photo')
async def photo_command(message: types.Message):
    caption = 'so cute cat :cat:'
    await bot.send_photo(message.from_user.id, PHOTO_WITH_CAT, caption=emojize(caption), reply_to_message_id=message.message_id)

@dp.message_handler(commands=['group'])
async def group_command(message: types.Message):
    media = [InputMediaVideo(VIDEO, 'puppies and cats')]
    for photo_id in KITTENS:
        media.append(InputMediaPhoto(photo_id))
    await bot.send_media_group(message.from_user.id, media)

@dp.message_handler(commands=['note'])
async def note_command(message: types.Message):
    await bot.send_chat_action(message.from_user.id, ChatActions.RECORD_VIDEO_NOTE)
    await asyncio.sleep(1)
    await bot.send_video_note(message.from_user.id, VIDEO_NOTE)

@dp.message_handler(commands=['file'])
async def file_command(message: types.Message):
    await bot.send_chat_action(message.from_user.id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(1)
    await bot.send_document(message.from_user.id, TEXT_FILE, caption='File for you')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
