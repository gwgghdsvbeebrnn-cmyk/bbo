import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv"9062280026:AAGRW6TqQ3y-VBHYqNIKps09szhKV04023Y "
bot = telebot.TeleBot(TOKEN)

ALMAZ = [
    ("100 + 10 бонус 💎 - 7.6 сомонӣ", "almaz_100", 7.6),
    ("310 + 16 бонус 💎 - 23 сомонӣ", "almaz_310", 23),
    ("520 + 52 бонус 💎 - 38 сомонӣ", "almaz_520", 38),
    ("1060 + 106 бонус 💎 - 76 сомонӣ", "almaz_1060", 76),
    ("2180 + 218 бонус 💎 - 152 сомонӣ", "almaz_2180", 152),
    ("5600 + 560 бонус 💎 - 380 сомонӣ", "almaz_5600", 380),
]
VOUCHER = [
    ("Ваучер Lite +90 💎 - 4 сомонӣ", "vouch_lite", 4),
    ("Ваучер Неделя +450 💎 - 15.5 сомонӣ", "vouch_week", 15.5),
    ("Ваучер Месяц +2600 💎 - 58 сомонӣ", "vouch_month", 58),
]

user_data = {}

def main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🛍 Магазин", callback_data="shop"),
        InlineKeyboardButton("🎟 Билеты", callback_data="tickets"),
        InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        InlineKeyboardButton("🏆 Рейтинг", callback_data="rating"),
        InlineKeyboardButton("🎰 Рулетка", callback_data="roulette"),
        InlineKeyboardButton("📦 Мои заказы", callback_data="my_orders"),
        InlineKeyboardButton("🎁 Розыгрыш", callback_data="giveaway"),
        InlineKeyboardButton("👥 Рефералы", callback_data="refs"),
        InlineKeyboardButton("⭐ Отзыв", callback_data="review"),
        InlineKeyboardButton("🆘 Поддержка 24/7", callback_data="support"),
    )
    return kb

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🐊 Добро пожаловать в CROKODIL!\n\n💎 Покупай алмазы Free Fire\n\nВыбирай действие 👇", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    chat = c.message.chat.id
    data = c.data
    bot.answer_callback_query(c.id)
    if data == "shop":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔥 Free Fire", callback_data="ff"))
        kb.add(InlineKeyboardButton("« Назад в меню", callback_data="back_main"))
        bot.edit_message_text("🛍 Магазин\n\nВыберите игру:", chat, c.message.message_id, reply_markup=kb)
    elif data == "back_main":
        bot.edit_message_text("Выбирай действие 👇", chat, c.message.message_id, reply_markup=main_kb())
    elif data == "ff":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("💎 Алмазы", callback_data="almaz_list"))
        kb.add(InlineKeyboardButton("🎫 Ваучеры", callback_data="voucher_list"))
        kb.add(InlineKeyboardButton("« Назад", callback_data="shop"))
        bot.edit_message_text("📍 Free Fire (CIS)\n\nВыберите:", chat, c.message.message_id, reply_markup=kb)
    elif data == "almaz_list":
        kb = InlineKeyboardMarkup()
        for txt, cd, _ in ALMAZ:
            kb.add(InlineKeyboardButton(txt, callback_data=cd))
        kb.add(InlineKeyboardButton("« Назад", callback_data="ff"))
        bot.edit_message_text("💎 Алмазы\n\nВыберите пакет:", chat, c.message.message_id, reply_markup=kb)
    elif data == "voucher_list":
        kb = InlineKeyboardMarkup()
        for txt, cd, _ in VOUCHER:
            kb.add(InlineKeyboardButton(txt, callback_data=cd))
        kb.add(InlineKeyboardButton("« Назад", callback_data="ff"))
        bot.edit_message_text("🎫 Ваучеры\n\nВыберите пакет:", chat, c.message.message_id, reply_markup=kb)
    elif data.startswith("almaz_") or data.startswith("vouch_"):
        all_items = {cd: (txt, price) for txt, cd, price in ALMAZ + VOUCHER}
        txt, price = all_items[data]
        user_data[chat] = {"item": txt, "price": price, "qty": 1, "name": txt}
        show_buy(chat, c.message.message_id, txt, price, 1)
    elif data == "plus":
        d = user_data.get(chat)
        if d:
            d["qty"] += 1
            show_buy(chat, c.message.message_id, d["name"], d["price"], d["qty"])
    elif data == "minus":
        d = user_data.get(chat)
        if d and d["qty"] > 1:
            d["qty"] -= 1
            show_buy(chat, c.message.message_id, d["name"], d["price"], d["qty"])
    elif data == "buy":
        d = user_data.get(chat)
        if d:
            bot.send_message(chat, f"🎮 {d['name']}\n💰 Цена: {d['price']*d['qty']:.2f} сомонӣ\n\nВведите ваш Free Fire ID (только цифры):")
            bot.register_next_step_handler_by_chat_id(chat, get_id)
    elif data == "profile":
        bot.send_message(chat, f"👤 Профиль\nID: {chat}\n💰 Баланс: 0 сомонӣ")
    elif data == "support":
        bot.send_message(chat, "🆘 Поддержка 24/7\nНапишите: @fakirov_09")
    else:
        bot.send_message(chat, "Скоро будет! 🔥")

def show_buy(chat, msg_id, name, price, qty):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("➖", callback_data="minus"),
        InlineKeyboardButton(f"Кол-во: {qty}", callback_data="none"),
        InlineKeyboardButton("➕", callback_data="plus"),
    )
    kb.add(InlineKeyboardButton(f"Купить ({qty} шт.) - {price*qty:.2f} сомонӣ", callback_data="buy"))
    kb.add(InlineKeyboardButton("« Назад", callback_data="ff"))
    bot.edit_message_text(f"📍 Free Fire (CIS)\n\n🎮 {name}\n💰 Цена: {price} сомонӣ\n⏰ Зачисление: 1-5 минут", chat, msg_id, reply_markup=kb)

def get_id(m):
    if not m.text.isdigit():
        bot.send_message(m.chat.id, "❌ Только цифры! Еще раз:")
        bot.register_next_step_handler_by_chat_id(m.chat.id, get_id)
        return
    d = user_data.get(m.chat.id, {})
    total = d.get("price", 0) * d.get("qty", 1)
    bot.send_message(m.chat.id, f"✅ Заказ принят!\n\n🎮 {d.get('name')}\n🆔 ID: {m.text}\n💰 К оплате: {total:.2f} сомонӣ\n\n💳 Для оплаты - Alif:\n📱 939992242\n\n📤 После оплаты чек отправьте сюда: @fakirov_09")

print("Бот кор карда истодааст...")
bot.infinity_polling()
