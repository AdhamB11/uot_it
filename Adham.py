import logging
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler

# تطبيق nest_asyncio للسماح بتشغيل event loop
nest_asyncio.apply()

# ملف لتخزين الأرقام
user_numbers_file = "user_numbers.txt"

# معرف المستخدم الخاص بك
ADMIN_USER_ID = 5875039604  # استبدل هذا بمعرفك الحقيقي

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

def is_valid_number(number: str) -> bool:
    if len(number) != 10 or not number.isdigit():
        return False
    if number[3:6] not in ["180", "181"]:
        return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! من فضلك، أدخل رقم القيد الخاص بك.")

async def process_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text
    user_id = update.effective_user.id

    if is_valid_number(number):
        user_numbers = []
        try:
            with open(user_numbers_file, "r") as file:
                user_numbers = [line.strip().split(',') for line in file.readlines()]
        except FileNotFoundError:
            pass

        for entry in user_numbers:
            if entry[0] == number and entry[1] != str(user_id):
                await update.message.reply_text("هذا الرقم مستخدم من قبل مستخدم آخر.")
                return await start(update, context)

        with open(user_numbers_file, "a") as file:
            file.write(f"{number},{user_id}\n")

        await update.message.reply_text(f"تم إضافة الرقم: {number}")
        await show_buttons(update, context)
    else:
        await update.message.reply_text("رقم القيد غير صحيح. تأكد من أنه مكون من 10 أرقام وأن الأرقام الرابعة والخامسة والسادسة هي 180 أو 181.")
        return await start(update, context)

async def list_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_USER_ID:
        try:
            with open(user_numbers_file, "r") as file:
                user_numbers = [line.strip() for line in file.readlines()]
                if user_numbers:
                    await update.message.reply_text("الأرقام المستخدمة:\n" + "\n".join(user_numbers))
                else:
                    await update.message.reply_text("لا توجد أرقام مستخدمة.")
        except FileNotFoundError:
            await update.message.reply_text("لم يتم العثور على ملف الأرقام.")
    else:
        await update.message.reply_text("ليس لديك إذن لاستخدام هذا الأمر.")

async def show_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("مقدمة في البرمجة", callback_data='intro_programming')],
        [InlineKeyboardButton("البرمجة الشيئية", callback_data='object_oriented')],
        [InlineKeyboardButton("معمارية الحاسوب", callback_data='computer_architecture')],
        [InlineKeyboardButton("تراكيب البيانات", callback_data='data_structures')],
        [InlineKeyboardButton("مقدمة في قواعد البيانات", callback_data='db_intro')],
        [InlineKeyboardButton("التحليل العددي", callback_data='numerical_analysis')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر درسًا:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"You selected: {query.data}")

def main():
    application = ApplicationBuilder().token("7598541449:AAEJ1F65JP8Er3o_7ao4H8RepyScvbGv_U0").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(None, process_number))
    application.add_handler(CommandHandler("list_numbers", list_numbers))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if name == "main":
    main()
