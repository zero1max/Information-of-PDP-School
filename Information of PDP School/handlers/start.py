from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart, Command
from loader import router, bot, db
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.defoult.keybords import * 

ADMIN = "ADMIN_ID"

class MSG(StatesGroup):
    messaga = State()

class Answer(StatesGroup):
    asnwer = State()

class Users(StatesGroup):
    name = State()
    raqam = State() 


@router.message(CommandStart())
async def start(msg: Message):
    if msg.from_user.id == ADMIN:
        await msg.answer(f"<b>Assalomu aleykum {msg.from_user.full_name}!</b>\n\n/users - userlarni ko'rish")
        # user_info = db.select_users()
        # if user_info:
        #     await msg.answer("Foydalanuvchilar ro'yxati:")
        #     for user in user_info:
        #         user_id, name, raqam = user
        #         await msg.answer(f"Foydalanuvchi ID: {user_id}\nIsm: {name}\nRaqam: {raqam}")   
    else:
        await msg.answer(f"Assalomu aleykum {msg.from_user.full_name}!", reply_markup=menu)
    db.create_table()

@router.message(Command('users'))
async def sel_users(msg: Message):
    if msg.from_user.id == ADMIN:
        user_info = db.select_users()
        if user_info:
            await msg.answer("Foydalanuvchilar ro'yxati:")
            for user in user_info:
                user_id, name, raqam = user
                await msg.answer(f"Foydalanuvchi ID: {user_id}\nIsm: {name}\nRaqam: {raqam}") 
        if not user_info:
            await msg.answer("Hech qanday user topilmadi")  # No user found message
    else:
        await msg.answer("No user")  


@router.message(Command("help"))
async def yordam(msg: Message):
    await msg.answer(f"Savollaringiz bo'lsa <b>@zero_1_max</b> ga murojat qiling")

#-------------------- Register ---------------------
@router.message(F.text == "Ro'yhatdan o'tish📋")
async def fio(msg: Message, state: FSMContext):
    await state.set_state(Users.name)
    await msg.answer("Familya, Ism va Otangizning ismini yuboring:\nMisol uchun: <b>Umarov Ali Sadullayev</b>")
   

@router.message(Users.name)
async def nomer(msg: Message, state: FSMContext):
    await state.update_data(name= msg.text)
    await state.set_state(Users.raqam)
    await msg.answer("Telefon raqamingizni yuboring!", reply_markup=tel)    

@router.message(Users.raqam, F.contact)
async def users_name(msg: Message, state: FSMContext):
    contact = msg.contact
    await state.update_data(raqam=contact)
    data = await state.get_data()
    name = data.get('name')
    raqam = data.get('raqam').phone_number if data.get('raqam') else None
    print(name)
    print(raqam)
    await state.clear()
    await msg.answer("Ro'yxatdan o'tildi!✅", reply_markup=menu1)
    db.add_user(name, raqam)

# ---------------- Chat ------------------
@router.message(F.text == "Savol yuborish✍🏻")
async def get_msg(msg: Message, state: FSMContext):
    await state.set_state(MSG.messaga)
    await msg.answer(f"Savollaringizni yuboring {msg.from_user.full_name}!")

@router.message(MSG.messaga)
async def question(msg: Message, state: FSMContext):
    await msg.answer("Admin tez oradi sizga javob qaytaradi!")
    text = msg.text
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    answer_btn = InlineKeyboardButton(text='Javob qaytarish', callback_data=f'answer:{user_id}')
    answer_key = InlineKeyboardMarkup(inline_keyboard=[[answer_btn]])
    await bot.send_message(chat_id=ADMIN, text=f"Savol yuboruvchi: {user_name}\nSavol: {text}", reply_markup=answer_key)
    await state.clear()

@router.callback_query(F.data.startswith('answer:'))
async def answeruser(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(':')
    await state.update_data(user_id = user_id[1])
    await state.set_state(Answer.asnwer)
    await bot.send_message(ADMIN, text= f"ID: {user_id[1]}\nJavob yozishingiz mumkin Muhammadjon")

@router.message(Answer.asnwer)
async def answer(msg:Message, state:FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id = int(data['user_id']), text=f"<b>Admindan javob:</b>\n{msg.text}\n\n<b>Savolingiz uchun rahmat!</b>", reply_markup=menu1)
    
# -------------------- Savol yuborish--------------
@router.message(F.text == "Savol yubormoqchiman✍🏻")
async def add_ques(msg: Message):
    await msg.answer("Iltimos avval ro'yxatdan o'ting!", reply_markup=register)

#---------------------Info------------------
@router.message(F.text == 'Info📝')
async def info(msg: Message):
    await msg.answer('<b>PDP School haqida qisqacha</b>')
    await bot.send_photo(msg.from_user.id ,photo='https://optim.tildacdn.com/tild3964-3038-4639-b439-326435396236/-/format/webp/1.jpg', caption=f"<b>📚Talab yuqori bo‘lgan “IT” sohasiga ixtisoslashgan ta’lim tizimi!\n\n📊Dasturchi kadrlar yetishtirishda 6 yillik tajribaga ega tizim ustida qurilgan\n\n🤼‍♀️Sog‘lom kun tartibiga asoslangan sport mashg‘ulotlari va maxsus menyu\n\n📷Farzandlaringiz salomatligi va xavfsizligi nazorati\n\n📖Ingliz tili va Matematika fanlari bilan boyitilgan ta’lim dasturlari</b>")
    #await msg.answer(f"<b>📚Talab yuqori bo‘lgan “IT” sohasiga ixtisoslashgan ta’lim tizimi!\n\n📊Dasturchi kadrlar yetishtirishda 6 yillik tajribaga ega tizim ustida qurilgan\n\n🤼‍♀️Sog‘lom kun tartibiga asoslangan sport mashg‘ulotlari va maxsus menyu\n\n📷Farzandlaringiz salomatligi va xavfsizligi nazorati\n\n📖Ingliz tili va Matematika fanlari bilan boyitilgan ta’lim dasturlari</b>")
    await msg.answer("<b>PDP raqamlarda</b>")
    await msg.answer(f"PDP — Oʻzbekistonda IT mutaxassislar elitasini shakllantirishni oʻz oldiga maqsad qilib qoʻygan ekotizimdir.\n\n📆<b>6-yil</b>\nIT mutaxassislarni tayyorlashda tajriba\n\n<b>💵$500</b>\nBitiruvchining oʻrtacha boshlang’ich oylik maoshi\n\n🖥<b>10+</b>\nPDP — 10 dan ziyod IT kompaniya va bir qancha loyihalarga ega ekotizimdir.\n\n<b>👨🏻‍💻50+</b>\nAmaliyot o’tash va ishga joylashish uchun 50 dan ziyod nufuzli IT kompaniyalar bilan hamkordir\n\n✅<b>90%</b>\nOʻrtacha ishga joylashish koeffitsienti\n\n👨‍🎓<b>2000+</b>\nPDP bitiruvchilar")

#----------------------Location------------------
@router.message(F.text == "Manzilni ko'rish📍")
async def locaton(msg: Message):
    latitude = 41.23437586925201  
    longitude = 69.21561572492116  
    await bot.send_location(msg.from_user.id, latitude=latitude, longitude=longitude)


#---------------------Contact------------------
@router.message(F.text == "Biz bilan bog'lanish📞")
async def boglanw(msg: Message):
    await msg.answer('Tanlang:', reply_markup=contact)

@router.message(F.text == 'Telefon raqam')
async def nomer(msg: Message):
    await bot.send_contact(msg.from_user.id, phone_number='+998787777474', first_name="PDP School")
    await msg.reply("Bog'lanish uchun telefon raqam👆🏻")

@router.message(F.text == 'Telegram')
async def tg(msg: Message):
    await bot.send_message(msg.from_user.id, 'https://t.me/pdpschooluz')
    await msg.reply('Telegram uchun silka👆🏻')

@router.message(F.text == 'Web-sayt')
async def web(msg: Message):
    await bot.send_message(msg.from_user.id, "https://school.pdp.uz/")
    await msg.reply('Web-sayt uchun silka👆🏻')

@router.message(F.text == 'Facebook')
async def facebook(msg: Message):
    await bot.send_message(msg.from_user.id, 'https://www.facebook.com/pdp.schooluz')
    await msg.reply('Facebook uchun silka👆🏻')


@router.message(F.text == 'Instagram')
async def instagram(msg: Message):
    await bot.send_message(msg.from_user.id, 'https://www.instagram.com/pdp.school')
    await msg.reply('Instagram uchun silka👆🏻')


#--------------------- Asosiy Menu-----------------
@router.message(F.text == "Asosiy menu🏠")
async def back(msg: Message):
    await msg.answer("Asosiy menu🏠", reply_markup=menu)

#------------------------Nothing----------------
@router.message()
async def nothing(msg: Message):
    await msg.answer('Cunmadim?')