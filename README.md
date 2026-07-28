import logging
import re
import json
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    PicklePersistence,
    filters,
)

# Logging ማስተካካያ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ---------------- 1. አስፈላጊ መረጃዎች ----------------
BOT_TOKEN = '8657121840:AAE3j8mgmvn3OC6k9K-jO5gPCudxA_9Gzyw'  # የእርስዎ Bot Token
ADMIN_ID = 8369706951  # የአድሚኑ Telegram Chat ID (ቁጥር ብቻ)

CBA_ACCOUNT = "1000527085024"
ACCOUNT_NAME = "Daniel"

PRICE_PDF_TO_ID = 25.0  # የ PDF to ID ዋጋ
PRICE_16_DIGIT = 50.0   # የ 16 አስገባ ዋጋ

DATA_FILE = "user_balances.json"

# ---------------- ዳታቤዝ (JSON File) ማስቀመጫ እና ማንበቢያ ----------------
def load_balances():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return {int(k): float(v) for k, v in data.items()}
        except Exception as e:
            logging.error(f"ዳታ ማንበብ አልተቻለም: {e}")
            return {}
    return {}

def save_balances():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(user_balances, f)
    except Exception as e:
        logging.error(f"ዳታ ማስቀመጥ አልተቻለም: {e}")

user_balances = load_balances()

# የ Conversation ደረጃዎች (States)
(
    CHOOSE_MENU, 
    CHOOSE_BANK, 
    CHOOSE_AMOUNT, 
    WAIT_TX_ID, 
    WAIT_16_DIGIT, 
    WAIT_OTP,
    WAIT_PDF_CONVERT
) = range(7)


# /start ትዕዛዝ ሲነካ (ለመጀመሪያ ጊዜ ብቻ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in user_balances:
        user_balances[user.id] = 0.0
        save_balances()

    keyboard = [
        [KeyboardButton("Deposit"), KeyboardButton("Balance")],
        [KeyboardButton("16 አስገባ"), KeyboardButton("📄 PDF to ID")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"እንኳን ደህና መጡ {user.first_name}! እባክዎን ከታች ካሉት አማራጮች አንዱን ይምረጡ፡",
        reply_markup=reply_markup,
    )
    return CHOOSE_MENU


async def back_to_menu(update: Update):
    keyboard = [
        [KeyboardButton("Deposit"), KeyboardButton("Balance")],
        [KeyboardButton("16 አስገባ"), KeyboardButton("📄 PDF to ID")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("ወደ ዋናው ሜኑ ተመልሰዋል። እባክዎን ይምረጡ፡", reply_markup=reply_markup)
    return CHOOSE_MENU


# ---------------- ዋና ሜኑ ----------------
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    if text == "🔙 Back":
        return await back_to_menu(update)

    if text == "Balance":
        balance = user_balances.get(user.id, 0.0)
        await update.message.reply_text(f"💳 የነባር ዋሌት ባላንስዎ፡ {balance:.2f} ETB ነው::")
        return CHOOSE_MENU

    elif text == "Deposit":
        keyboard = [
            [KeyboardButton("የኢትዮጵያ ንግድ ባንክ (CBE)")],
            [KeyboardButton("🔙 Back")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "እባክዎን ክፍያ የሚፈጽሙበትን ባንክ ይምረጡ፡",
            reply_markup=reply_markup,
        )
        return CHOOSE_BANK

    elif text == "16 አስገባ":
        user_balance = user_balances.get(user.id, 0.0)

        if user_balance < PRICE_16_DIGIT:
            await update.message.reply_text(
                f"⚠️ **በቂ ባላንስ የለዎትም!**\n\n"
                f"የዚህ አገልግሎት ዋጋ **{PRICE_16_DIGIT:.2f} ETB** ሲሆን፣ የእርስዎ ባላንስ **{user_balance:.2f} ETB** ነው።\n"
                f"እባክዎን አስቀድመው **Deposit** በማድረግ ሂሳብዎን ይሙሉ::",
                parse_mode="Markdown"
            )
            return CHOOSE_MENU

        keyboard = [[KeyboardButton("🔙 Back")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        info_msg = (
            f"ℹ️ **የአገልግሎቱ ዋጋ {PRICE_16_DIGIT:.0f} ብር ነው::**\n\n"
            f"እባክዎን **የ 16 ዲጂት ቁጥሩን** ያስገቡ፡"
        )
        await update.message.reply_text(info_msg, parse_mode="Markdown", reply_markup=reply_markup)
        return WAIT_16_DIGIT

    elif text == "📄 PDF to ID":
        user_balance = user_balances.get(user.id, 0.0)

        if user_balance < PRICE_PDF_TO_ID:
            await update.message.reply_text(
                f"⚠️ **በቂ ባላንስ የለዎትም!**\n\n"
                f"የ PDF to ID አገልግሎት ዋጋ **{PRICE_PDF_TO_ID:.2f} ETB** ሲሆን፣ የእርስዎ ባላንስ **{user_balance:.2f} ETB** ነው።\n"
                f"እባክዎን አስቀድመው **Deposit** በማድረግ ሂሳብዎን ይሙሉ::",
                parse_mode="Markdown"
            )
            return CHOOSE_MENU

        keyboard = [[KeyboardButton("🔙 Back")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"ℹ️ **የ PDF to ID አገልግሎት ዋጋ {PRICE_PDF_TO_ID:.0f} ብር ነው::**\n\n"
            f"እባክዎን መቀየር የሚፈልጉትን **PDF ፋይል** እዚህ ይላኩ፡",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return WAIT_PDF_CONVERT

    else:
        await update.message.reply_text("እባክዎን የተሰጡትን አዝራሮች ብቻ ይጠቀሙ።")
        return CHOOSE_MENU


# ---------------- PDF TO ID FLOW ----------------
async def handle_pdf_convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if update.message.text and update.message.text == "🔙 Back":
        return await back_to_menu(update)

    if not update.message.document:
        await update.message.reply_text("⚠️ እባክዎን ትክክለኛ የ PDF ፋይል ይላኩ፡")
        return WAIT_PDF_CONVERT

    doc_file_id = update.message.document.file_id

    keyboard = [
        [
            InlineKeyboardButton("✅ ተቀበል", callback_data=f"pdfaccept_{user.id}_pdf"),
            InlineKeyboardButton("❌ አቋርጥ", callback_data=f"pdfreject_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    admin_caption = (
        f"📄 **አዲስ PDF to ID ጥያቄ ደርሷል!**\n\n"
        f"👤 ደንበኛ: {user.first_name} (@{user.username})\n"
        f"🆔 User ID: `{user.id}`\n"
        f"💰 የነባር ባላንስ: {user_balances.get(user.id, 0.0):.2f} ETB\n\n"
        f"እባክዎን አንዱን አማራጭ ይምረጡ፦"
    )

    try:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=doc_file_id,
            caption=admin_caption,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"ለአድሚን PDF መላክ አልተቻለም: {e}")

    # ወደ ዋናው ሜኑ አይመለስም፤ ባሉበት ይጠብቃሉ
    await update.message.reply_text(
        "⏳ መረጃዎ ለአስተዳዳሪው ደርሷል። እባክዎን አስተዳዳሪው እስኪያረጋግጥ ድረስ ባሉበት ይጠብቁ...🔄"
    )
    return WAIT_PDF_CONVERT


# ---------------- 16 DIGIT & OTP FLOW ----------------
async def handle_16_digit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    digit_text = update.message.text.strip() if update.message.text else ""
    if digit_text == "🔙 Back":
        return await back_to_menu(update)

    user = update.effective_user

    clean_digits = re.sub(r'\D', '', digit_text)
    if len(clean_digits) != 16:
        await update.message.reply_text("⚠️ እባክዎን ትክክለኛ የ 16 ዲጂት ቁጥር ያስገቡ፡")
        return WAIT_16_DIGIT

    context.user_data['digit_16'] = clean_digits

    # ለአድሚን ቶሎ መላክ
    admin_digit_msg = (
        f"🔢 **16 ዲጂት ቁጥር ቀጥታ ደርሷል!**\n\n"
        f"👤 ደንበኛ: {user.first_name} (@{user.username})\n"
        f"🆔 User ID: `{user.id}`\n"
        f"💳 16 ዲጂት: `{clean_digits}`"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_digit_msg, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"ለአድሚን መላክ አልተቻለም: {e}")

    keyboard = [[KeyboardButton("🔙 Back")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("✅ የ 16 ዲጂት ቁጥሩን ተቀብለናል። አሁን እባክዎን **OTP** ያስገቡ፡", reply_markup=reply_markup)
    return WAIT_OTP


async def handle_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp_code = update.message.text.strip() if update.message.text else ""
    if otp_code == "🔙 Back":
        return await back_to_menu(update)

    user = update.effective_user
    balance = user_balances.get(user.id, 0.0)
    digit_16 = context.user_data.get('digit_16', 'ያልታወቀ')

    keyboard = [
        [
            InlineKeyboardButton("✅ ተቀበል (PDF ላክ)", callback_data=f"pdfaccept_{user.id}_16digit"),
            InlineKeyboardButton("❌ አቋርጥ", callback_data=f"pdfreject_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    admin_otp_msg = (
        f"🔑 **አዲስ OTP ደርሷል!**\n\n"
        f"👤 ደንበኛ: {user.first_name} (@{user.username})\n"
        f"🆔 User ID: `{user.id}`\n"
        f"💳 16 ዲጂት: `{digit_16}`\n"
        f"🔢 OTP: `{otp_code}`\n"
        f"💰 የነባር ባላንስ: {balance:.2f} ETB\n\n"
        f"እባክዎን ያረጋግጡ፦"
    )
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_otp_msg,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"ለአድሚን መላክ አልተቻለም: {e}")

    # ባሉበት ይጠብቃሉ
    await update.message.reply_text("⏳ ጥያቄዎ ለአስተዳዳሪው ደርሷል። እባክዎን አስተዳዳሪው እስኪያረጋግጥ ድረስ ባሉበት ይጠብቁ...🔄")
    return WAIT_OTP


# ---------------- DEPOSIT FLOW ----------------
async def handle_bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Back":
        return await back_to_menu(update)

    if text == "የኢትዮጵያ ንግድ ባንክ (CBE)":
        keyboard = [
            [KeyboardButton("500"), KeyboardButton("1000")],
            [KeyboardButton("2000"), KeyboardButton("5000")],
            [KeyboardButton("10000")],
            [KeyboardButton("🔙 Back")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "እባክዎን ገቢ ማድረግ የሚፈልጉትን የብር መጠን ይምረጡ (ከ 500 እስከ 10,000 ብር)፡",
            reply_markup=reply_markup,
        )
        return CHOOSE_AMOUNT
    else:
        await update.message.reply_text("እባክዎን ትክክለኛ ባንክ ይምረጡ።")
        return CHOOSE_BANK


async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🔙 Back":
        return await back_to_menu(update)

    if not text.isdigit():
        await update.message.reply_text("እባክዎን ትክክለኛ የቁጥር መጠን ይምረጡ።")
        return CHOOSE_AMOUNT

    amount = int(text)
    if amount < 500 or amount > 10000:
        await update.message.reply_text("የብር መጠኑ ከ 500 እስከ 10,000 ብር ክልል ውስጥ መሆን አለበት።")
        return CHOOSE_AMOUNT

    context.user_data['deposit_amount'] = amount

    keyboard = [[KeyboardButton("🔙 Back")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    msg = (
        f"ለማስገባት የመረጡት መጠን፡ {amount} ETB\n\n"
        f"እባክዎን ወደሚከተለው የንግድ ባንክ ሂሳብ ገቢ ያድርጉ፡\n"
        f"🏦 **የሂሳብ ቁጥር:** `{CBA_ACCOUNT}`\n"
        f"👤 **የአካውንት ስም:** `{ACCOUNT_NAME}`\n\n"
        f"ክፍያውን ከፈጸሙ በኋላ የተቀበሉትን **Transaction ID** ወይም የደረሰኝ **Photo/PDF** እዚህ ይላኩት፡"
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)
    return WAIT_TX_ID


async def handle_tx_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message.text else ""
    if text == "🔙 Back":
        return await back_to_menu(update)

    amount = context.user_data.get('deposit_amount', 0)
    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton("✅ ልክ ነው", callback_data=f"approve_{user.id}_{amount}"),
            InlineKeyboardButton("❌ ልክ አይደለም", callback_data=f"reject_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    admin_msg = (
        f"📥 **አዲስ የ Deposit ማረጋገጫ ጥያቄ!**\n\n"
        f"👤 ደንበኛ: {user.first_name} (@{user.username})\n"
        f"🆔 User ID: `{user.id}`\n"
        f"💵 መጠን: {amount} ETB\n"
        f"🧾 Transaction ID: `{text}`\n\n"
        f"እባክዎን ክፍያውን አረጋግጠው አንዱን ይጫኑ፦"
    )
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_msg,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"ለአድሚን መላክ አልተቻለም: {e}")

    # ወደ ዋናው ሜኑ ሳይመለሱ ባሉበት ይቆያሉ
    await update.message.reply_text("⏳ መረጃዎ እየተጣራ ነው። እባክዎን አስተዳዳሪው እስኪያረጋግጥ ድረስ ባሉበት ይጠብቁ...🔄")
    return WAIT_TX_ID


# ---------------- የአድሚኑን ቁልፍ (Buttons) ማስተናገጃ Callback ----------------
async def admin_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    action = data[0]
    user_id = int(data[1])

    main_keyboard = [
        [KeyboardButton("Deposit"), KeyboardButton("Balance")],
        [KeyboardButton("16 አስገባ"), KeyboardButton("📄 PDF to ID")]
    ]
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

    # Deposit Approve
    if action == "approve":
        amount = float(data[2])
        user_balances[user_id] = user_balances.get(user_id, 0.0) + amount
        save_balances()
        await query.edit_message_text(text=f"{query.message.text}\n\n✅ **ተረጋግጧል (Approved)!**")

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"✅ ክፍያዎ በስኬት ተረጋግጧል!\n\n💰 {amount:.2f} ETB ወደ ሂሳብዎ ገቢ ሆኗል።\n💳 አሁን ያለዎት ቀሪ ሂሳብ፡ {user_balances[user_id]:.2f} ETB",
                reply_markup=reply_markup
            )
            # ክፍያው ሲረጋገጥ ብቻ ደንበኛውን ወደ ዋናው ሜኑ ይመልሰዋል
            context.application.drop_user_data(user_id)
        except Exception as e:
            logging.error(f"ለደንበኛ ማሳወቅ አልተቻለም: {e}")

    # Deposit Reject
    elif action == "reject":
        await query.edit_message_text(text=f"{query.message.text}\n\n❌ **ተሰርዟል (Rejected)!**")

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ ክፍያዎ አልተሳካም። ያስገቡት Transaction ID ትክክል አይደለም።\n\nእባክዎን እንደገና Deposit በመምረጥ ትክክለኛውን Transaction ID ደግመው ያስገቡ።",
                reply_markup=reply_markup
            )
        except Exception as e:
            logging.error(f"ለደንበኛ ማሳወቅ አልተቻለም: {e}")

    # PDF Accept
    elif action == "pdfaccept":
        req_type = data[2] if len(data) > 2 else "pdf"
        
        context.bot_data['target_pdf_user'] = user_id
        context.bot_data['request_type'] = req_type

        status_text = f"\n\n✅ **ጥያቄው ተቀባይነት አግኝቷል!** (አገልግሎት: {req_type})"
        if query.message.caption:
            await query.edit_message_caption(caption=f"{query.message.caption}{status_text}")
        else:
            await query.edit_message_text(text=f"{query.message.text}{status_text}")

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📥 **አሁን ለተጠቃሚው (`{user_id}`) የሚላከውን የተዘጋጀ PDF/ፋይል እዚህ ይላኩት፦**",
            parse_mode="Markdown"
        )

    # PDF Reject
    elif action == "pdfreject":
        status_text = "\n\n❌ **ጥያቄው ተሰርዟል!**"
        if query.message.caption:
            await query.edit_message_caption(caption=f"{query.message.caption}{status_text}")
        else:
            await query.edit_message_text(text=f"{query.message.text}{status_text}")

        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ ጥያቄዎ አልተቀበለም። ያስገቡት መረጃ ትክክል አይደለም፤ እባክዎን በድጋሜ ይሞክሩ።",
                reply_markup=reply_markup
            )
        except Exception as e:
            logging.error(f"ለደንበኛ ማሳወቅ አልተቻለም: {e}")


# ---------------- አድሚኑ ፋይል ሲልክ ለደንበኛው ማስተላለፊያ ----------------
async def handle_admin_reply_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    target_user_id = context.bot_data.get('target_pdf_user')
    req_type = context.bot_data.get('request_type', 'pdf')

    if not target_user_id:
        await update.message.reply_text("⚠️ ፋይል የሚላክለት ተጠቃሚ አልተገኘም። እባክዎን አስቀድመው ከላይ '✅ ተቀበል' የሚለውን ቁልፍ ይጫኑ።")
        return

    deduct_amount = PRICE_16_DIGIT if req_type == "16digit" else PRICE_PDF_TO_ID
    
    current_bal = user_balances.get(target_user_id, 0.0)
    user_balances[target_user_id] = max(0.0, current_bal - deduct_amount)
    save_balances()
    
    new_bal = user_balances[target_user_id]

    main_keyboard = [
        [KeyboardButton("Deposit"), KeyboardButton("Balance")],
        [KeyboardButton("16 አስገባ"), KeyboardButton("📄 PDF to ID")]
    ]
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

    sent_success = False

    if update.message.document:
        doc_id = update.message.document.file_id
        try:
            await context.bot.send_document(
                chat_id=target_user_id,
                document=doc_id,
                caption=(
                    f"✅ **የተዘጋጀው PDF ID ደርሷል!**\n\n"
                    f"💸 የተቆረጠ ሂሳብ፡ **{deduct_amount:.2f} ETB**\n"
                    f"💳 ቀሪ ሂሳብዎ፡ **{new_bal:.2f} ETB**"
                ),
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            sent_success = True
        except Exception as e:
            await update.message.reply_text(f"❌ ለተጠቃሚው መላክ አልተቻለም: {e}")

    elif update.message.photo:
        photo_id = update.message.photo[-1].file_id
        try:
            await context.bot.send_photo(
                chat_id=target_user_id,
                photo=photo_id,
                caption=(
                    f"✅ **የተዘጋጀው PDF ID ደርሷል!**\n\n"
                    f"💸 የተቆረጠ ሂሳብ፡ **{deduct_amount:.2f} ETB**\n"
                    f"💳 ቀሪ ሂሳብዎ፡ **{new_bal:.2f} ETB**"
                ),
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            sent_success = True
        except Exception as e:
            await update.message.reply_text(f"❌ ለተጠቃሚው መላክ አልተቻለም: {e}")

    else:
        await update.message.reply_text("⚠️ እባክዎን PDF ፋይል ወይም Document ብቻ ይላኩ።")
        return

    if sent_success:
        await update.message.reply_text(
            f"✅ ፋይሉ ለተጠቃሚው (`{target_user_id}`) በስኬት ተልኳል!\n"
            f"💰 ከደንበኛው **{deduct_amount:.2f} ETB** ተቆርጧል። ቀሪ ባላንሱ፡ **{new_bal:.2f} ETB** ነው::",
            parse_mode="Markdown"
        )
        context.bot_data['target_pdf_user'] = None
        context.bot_data['request_type'] = None


# ---------------- ፎቶ ማስተናገጃ (ለደንበኞች) ----------------
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id == ADMIN_ID:
        return await handle_admin_reply_pdf(update, context)

    photo_file_id = update.message.photo[-1].file_id

    caption = f"🖼 **አዲስ የፎቶ ደረሰኝ ደርሷል!**\n\n👤 ደንበኛ: {user.first_name} (@{user.username})\n🆔 User ID: `{user.id}`"
    try:
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file_id, caption=caption, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"ለአድሚን ፎቶ መላክ አልተቻለም: {e}")

    await update.message.reply_text("✅ ፎቶዎ ደርሶናል! አድሚኑ አረጋግጦ መልስ እስኪልክ ድረስ እባክዎን ይጠብቁ።")


def main():
    # ኔትወርክ ቢቋረጥም ደረጃዎችን (States) በፋይል መያዣ persistence ማዘጋጀት
    persistence = PicklePersistence(filepath="bot_state.pickle")

    app = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence).build()

    # 1. የአድሚን ፋይል አስተላላፊ
    app.add_handler(MessageHandler((filters.Document.ALL | filters.PHOTO) & filters.User(user_id=ADMIN_ID), handle_admin_reply_pdf))

    # 2. Inline Buttons handler
    app.add_handler(CallbackQueryHandler(admin_button_callback, pattern="^(approve|reject|pdfaccept|pdfreject)_"))

    # 3. Conversation Handler (ለደንበኞች) - name እና persistent ተጨምሮበታል
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            CHOOSE_BANK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bank)],
            CHOOSE_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount)],
            WAIT_TX_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tx_id)],
            WAIT_16_DIGIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_16_digit)],
            WAIT_OTP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_otp)],
            WAIT_PDF_CONVERT: [
                MessageHandler(filters.Document.ALL, handle_pdf_convert),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_pdf_convert)
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        name="user_conversation",
        persistent=True
    )

    app.add_handler(conv_handler)

    # 4. Photo Handler (ለደንበኞች)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("ቦቱ እየሰራ ነው...")
    app.run_polling()


if __name__ == "__main__":
    main()
