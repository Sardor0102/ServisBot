from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton
from os import getenv
from dotenv import load_dotenv

load_dotenv("util/.env")
dp = Dispatcher()