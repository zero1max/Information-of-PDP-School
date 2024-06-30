from aiogram import Dispatcher, Router, Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from database.db_handlers import Database
from data.config import BOT_TOKEN

db = Database()
dp = Dispatcher()
router = Router()

# Initialize the bot with DefaultBotProperties
bot = Bot(
    token=BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.include_router(router=router)
