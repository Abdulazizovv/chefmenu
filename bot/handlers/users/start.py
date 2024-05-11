from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.loader import dp
import re
from bot.utils.db_api.db import add_user, check_user_exists
from bot.utils.helper import get_verification_code_async

kb_request_phone = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_request_phone = types.KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
kb_request_phone.add(btn_request_phone)

photo_id = "AgACAgIAAxkBAAMRZj-Q2OAAAWB11N1DZp9TupuIR-NLAAIU2zEbNJ34SSr5LspJFV5PAQADAgADeAADNQQ"


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    phone_number = await check_user_exists(message.from_user.id)
    if phone_number:
        code = await get_verification_code_async(phone_number[4:])
        if code:
            await message.answer(f"Tasdiqlash kodingiz: {code}\nKodni qaytadan olish uchun /verify buyrug'ini bering", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer_photo(photo_id, caption="Sizda tasdiqlash kodi mavjud emas! Ro'yxatdan o'tish qismidagi \"kodni yuborish\" tugmasini bosganingizni tekshiring", reply_markup=types.ReplyKeyboardRemove())
    # salomlashish xabari
    else:
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n"\
                            "Tasdiqlash kodni olish uchun telefon raqamingizni yuboring.", reply_markup=kb_request_phone)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def bot_get_contact(message: types.Message):
    contact = message.contact
    phone_number = contact.phone_number
    if phone_number[0] != "+":
        phone_number = f"+{phone_number}"

    # Validate phone number for Uzbekistan
    if re.match(r'^(\+)?998\d{9}$', phone_number):
        await add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            phone_number=phone_number,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code,
            is_bot=message.from_user.is_bot
        )
        await message.answer("Telefon raqamingiz qabul qilindi.", reply_markup=types.ReplyKeyboardRemove())
        code = await get_verification_code_async(phone_number[4:])
        if code:
            await message.answer(f"Tasdiqlash kodingiz: {code}\nKodni qaytadan olish uchun /verify buyrug'ini bering")
    else:
        await message.answer("Xizmat hozircha faqat O'zbekiston uchun mavjud. Iltimos, O'zbekiston raqamini kiriting.")


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def bot_get_photo(message: types.Message):
    await message.answer(message.photo[-1].file_id)
