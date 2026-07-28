import telebot
from telebot import types
import os

TOKEN ='8671641415:AAGZMyWB6J7_aAP0BPQlC3AsazoSCXVk0hk'
MY_ADMIN_ID = 8369706951

bot = telebot.TeleBot(TOKEN)

user_states = {}
user_language = {} # 'am', 'en', 'om', 'ti', 'so', 'ar', 'zh'
user_consult_item = {} # ለማማከር የተመረጠውን እቃ ለመያዝ
user_warranty_item = {} # ለዋስትና የተመረጠውን እቃ ለመያዝ
user_warranty_desc = {} # የዋስትና ብልሽት መግለጫ ለመያዝ

def save_user(user_id):
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()
    
    with open("users.txt", "r") as f:
        users = f.read().splitlines()
    
    if str(user_id) not in users:
        with open("users.txt", "a") as f:
            f.write(f"{user_id}\n")

# --- 🔙 የተመለስ አዝራር በቋንቋ መመለሻ ---
def get_back_button_text(lang='am'):
    if lang == 'en': return "⬅️ Back to Main Menu"
    elif lang == 'om': return "⬅️ Gara Menu Guddaatti"
    elif lang == 'ti': return "⬅️ ናብ ዋና ሜኑ ምለስ"
    elif lang == 'so': return "⬅️ Ku Noqo Liiska Weyn"
    elif lang == 'ar': return "⬅️ العودة إلى القائمة الرئيسية"
    elif lang == 'zh': return "⬅️ 返回主菜单"
    else: return "⬅️ ወደ ዋና ሜኑ"

# --- 🌐 የቋንቋ መምረጫ ሜኑ ---
def language_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add("🇪🇹 አማርኛ", "🇬🇧 English", "🌳 Afaan Oromoo")
    markup.add("🇪🇷 ትግርኛ", "🇸🇴 Soomaaliga", "🇸🇦 العربية", "🇨🇳 中文")
    return markup

# --- 🏠 የዋና ሜኑ አዝራሮች ---
def main_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        btn_buy = types.KeyboardButton("🛒 Shop")
        btn_repair = types.KeyboardButton("🛠️ Maintenance")
        btn_warranty = types.KeyboardButton("🛡️ Warranty Service")
        btn_choose = types.KeyboardButton("📦 Choose Items")
        btn_consult = types.KeyboardButton("📞 Consultation")
        btn_services = types.KeyboardButton("🛠️ Services")
        btn_phone = types.KeyboardButton("📞 Phone")
        btn_address = types.KeyboardButton("📍 Location")
        btn_feedback = types.KeyboardButton("💬 Feedback")
        btn_lang = types.KeyboardButton("🌐 Change Language")
    elif lang == 'om':
        btn_buy = types.KeyboardButton("🛒 Meeshaa Bitachuuf")
        btn_repair = types.KeyboardButton("🛠️ Meeshaa Suphsiisuuf")
        btn_warranty = types.KeyboardButton("🛡️ Tajaajila Wabii (Warranty)")
        btn_choose = types.KeyboardButton("📦 Meeshaa Filachuuf")
        btn_consult = types.KeyboardButton("📞 Mari'achuuf")
        btn_services = types.KeyboardButton("🛠️ Tajaajiloota")
        btn_phone = types.KeyboardButton("📞 Lakkoofsa Bilbilaa")
        btn_address = types.KeyboardButton("📍 Teessoo")
        btn_feedback = types.KeyboardButton("💬 Yaada")
        btn_lang = types.KeyboardButton("🌐 Afaan Jijjiiruuf")
    elif lang == 'ti':
        btn_buy = types.KeyboardButton("🛒 ንግዛእ ንብረት")
        btn_repair = types.KeyboardButton("🛠️ ንብረት ንምዕራይ")
        btn_warranty = types.KeyboardButton("🛡️ ኣገልግሎት ውሕስና (Warranty)")
        btn_choose = types.KeyboardButton("📦 ንብረት ንምረጽ")
        btn_consult = types.KeyboardButton("📞 ምኽሪ ንግበር")
        btn_services = types.KeyboardButton("🛠️ ኣገልግሎታት")
        btn_phone = types.KeyboardButton("📞 ቁጽሪ ስልኪ")
        btn_address = types.KeyboardButton("📍 ኣድራሻ")
        btn_feedback = types.KeyboardButton("💬 ርእይቶ")
        btn_lang = types.KeyboardButton("🌐 ቋንቋ ንምቕያር")
    elif lang == 'so':
        btn_buy = types.KeyboardButton("🛒 Iibsashada Alaabta")
        btn_repair = types.KeyboardButton("🛠️ Dayactirka Alaabta")
        btn_warranty = types.KeyboardButton("🛡️ Adeegga Damaanadda")
        btn_choose = types.KeyboardButton("📦 Dooro Alaabta")
        btn_consult = types.KeyboardButton("📞 La Tashiga")
        btn_services = types.KeyboardButton("🛠️ Adeegyada")
        btn_phone = types.KeyboardButton("📞 Lambarka Taleefanka")
        btn_address = types.KeyboardButton("📍 Goobta")
        btn_feedback = types.KeyboardButton("💬 Ra'yigaaga")
        btn_lang = types.KeyboardButton("🌐 Beddel Luqadda")
    elif lang == 'ar':
        btn_buy = types.KeyboardButton("🛒 شراء البضائع")
        btn_repair = types.KeyboardButton("🛠️ صيانة الأجهزة")
        btn_warranty = types.KeyboardButton("🛡️ خدمة الضمان")
        btn_choose = types.KeyboardButton("📦 اختر العناصر")
        btn_consult = types.KeyboardButton("📞 الاستشارة")
        btn_services = types.KeyboardButton("🛠️ الخدمات")
        btn_phone = types.KeyboardButton("📞 رقم الهاتف")
        btn_address = types.KeyboardButton("📍 الموقع")
        btn_feedback = types.KeyboardButton("💬 ملاحظاتك")
        btn_lang = types.KeyboardButton("🌐 تغير اللغات")
    elif lang == 'zh':
        btn_buy = types.KeyboardButton("🛒 购买商品")
        btn_repair = types.KeyboardButton("🛠️ 设备维修")
        btn_warranty = types.KeyboardButton("🛡️ 保修服务")
        btn_choose = types.KeyboardButton("📦 选择商品")
        btn_consult = types.KeyboardButton("📞 咨询服务")
        btn_services = types.KeyboardButton("🛠️ 我们的服务")
        btn_phone = types.KeyboardButton("📞 电话号码")
        btn_address = types.KeyboardButton("📍 地址")
        btn_feedback = types.KeyboardButton("💬 用户反馈")
        btn_lang = types.KeyboardButton("🌐 更改语言")
    else:
        btn_buy = types.KeyboardButton("🛒 ዕቃ ለመግዛት")
        btn_repair = types.KeyboardButton("🛠️ ዕቃ ለማሠራት")
        btn_warranty = types.KeyboardButton("🛡️ የዋስትና አገልግሎት")
        btn_choose = types.KeyboardButton("📦 እቃ ለመምረጥ")
        btn_consult = types.KeyboardButton("📞 ለማማከር")
        btn_services = types.KeyboardButton("🛠️ አገልግሎቶች")
        btn_phone = types.KeyboardButton("📞 ስልክ ቁጥር")
        btn_address = types.KeyboardButton("📍 አድራሻ")
        btn_feedback = types.KeyboardButton("💬 አስተያየት")
        btn_lang = types.KeyboardButton("🌐 ቋንቋ ለመቀየር")
    
    markup.add(btn_buy, btn_repair)
    markup.add(btn_warranty)
    markup.add(btn_choose, btn_consult)
    markup.add(btn_services, btn_phone)
    markup.add(btn_address, btn_feedback)
    markup.add(btn_lang)
    return markup

# --- 🛡️ የዋስትና እቃ መምረጫ ሜኑ ---
def warranty_item_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Fridge (Warranty)", "TV (Warranty)")
        markup.add("Oven (Warranty)", "Washing Machine (Warranty)")
        markup.add("Water Filter (Warranty)", "TV Stand (Warranty)")
        markup.add("Sofa Table (Warranty)")
    else:
        markup.add("ፍሪጅ (ዋስትና)", "ቲቪ (ዋስትና)")
        markup.add("ኦቭን (ዋስትና)", "ልብስ ማጠቢያ (ዋስትና)")
        markup.add("ውሀ ማጣሪያ (ዋስትና)", "ቲቪ ስታንድ (ዋስትና)")
        markup.add("የሶፋ ቴብል (ዋስትና)")
    markup.add(get_back_button_text(lang))
    return markup

# --- 📞 ለማማከር የእቃ መምረጫ ሜኑ ---
def consult_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Fridge (Consult)", "TV (Consult)")
        markup.add("Oven (Consult)", "Washing Machine (Consult)")
        markup.add("Water Filter (Consult)", "TV Stand (Consult)")
        markup.add("Sofa Table (Consult)")
    elif lang == 'om':
        markup.add("Firijii (Mari'achuuf)", "TV (Mari'achuuf)")
        markup.add("Oven (Mari'achuuf)", "Maashina Uffataa (Mari'achuuf)")
        markup.add("Calaltuu Bishaanii (Mari'achuuf)", "TV Stand (Mari'achuuf)")
        markup.add("Minoo Soofaa (Mari'achuuf)")
    elif lang == 'ti':
        markup.add("ፍሪጅ (ምኽሪ)", "ቲቪ (ምኽሪ)")
        markup.add("ኦቭን (ምኽሪ)", "ማሕጸቢ ክዳን (ምኽሪ)")
        markup.add("ጽሩይ ማይ ማጣሪያ (ምኽሪ)", "ቲቪ ስታንድ (ምኽሪ)")
        markup.add("ሶፋ ጠረጴዛ (ምኽሪ)")
    elif lang == 'so':
        markup.add("Qaboojiyaha (La Tashi')", "TV-ga (La Tashi')")
        markup.add("Oven-ka (La Tashi')", "Mashiinka Dharka (La Tashi')")
        markup.add("Sifeeyaha Biyaha (La Tashi')", "TV Stand (La Tashi')")
        markup.add("Miiska Fadhiga (La Tashi')")
    elif lang == 'ar':
        markup.add("ثلاجة (استشارة)", "تلفزيون (استشارة)")
        markup.add("فرن (استشارة)", "غسالة ملابس (استشارة)")
        markup.add("فلتر مياه (استشارة)", "حامل تلفزيون (استشارة)")
        markup.add("طاولة صوفا (استشارة)")
    elif lang == 'zh':
        markup.add("冰箱咨询", "电视咨询")
        markup.add("烤箱咨询", "洗衣机咨询")
        markup.add("净水器咨询", "电视柜咨询")
        markup.add("沙发桌咨询")
    else:
        markup.add("ፍሪጅ (ለማማከር)", "ቲቪ (ለማማከር)")
        markup.add("ኦቭን (ለማማከር)", "ልብስ ማጠቢያ (ለማማከር)")
        markup.add("ውሀ ማጣሪያ (ለማማከር)", "ቲቪ ስታንድ (ለማማከር)")
        markup.add("የሶፋ ቴብል (ለማማከር)")
    markup.add(get_back_button_text(lang))
    return markup

# --- 🛒 ለመግዛት ንኡስ ሜኑ ---
def buy_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Fridge (Buy)", "TV (Buy)")
        markup.add("Oven (Buy)", "Washing Machine (Buy)")
        markup.add("Water Filter (Buy)", "TV Stand (Buy)")
        markup.add("Sofa Table (Buy)")
    elif lang == 'om':
        markup.add("Firijii (Bitachuuf)", "TV (Bitachuuf)")
        markup.add("Oven (Bitachuuf)", "Maashina Uffataa (Bitachuuf)")
        markup.add("Calaltuu Bishaanii (Bitachuuf)", "TV Stand (Bitachuuf)")
        markup.add("Minoo Soofaa (Bitachuuf)")
    elif lang == 'ti':
        markup.add("ፍሪጅ (ንግዛእ)", "ቲቪ (ንግዛእ)")
        markup.add("ኦቭን (ንግዛእ)", "ማሕጸቢ ክዳን (ንግዛእ)")
        markup.add("ጽሩይ ማይ ማጣሪያ (ንግዛእ)", "ቲቪ ስታንድ (ንግዛእ)")
        markup.add("ሶፋ ጠረጴዛ (ንግዛእ)")
    elif lang == 'so':
        markup.add("Qaboojiyaha (Iibso)", "TV-ga (Iibso)")
        markup.add("Oven-ka (Iibso)", "Mashiinka Dharka (Iibso)")
        markup.add("Sifeeyaha Biyaha (Iibso)", "TV Stand (Iibso)")
        markup.add("Miiska Fadhiga (Iibso)")
    elif lang == 'ar':
        markup.add("ثلاجة (شراء)", "تلفزيون (شراء)")
        markup.add("فرن (شراء)", "غسالة ملابس (شراء)")
        markup.add("فلتر مياه (شراء)", "حامل تلفزيون (شراء)")
        markup.add("طاولة صوفا (شراء)")
    elif lang == 'zh':
        markup.add("冰箱 (购买)", "电视 (购买)")
        markup.add("烤箱 (购买)", "洗衣机 (购买)")
        markup.add("净水器 (购买)", "电视柜 (购买)")
        markup.add("沙发桌 (购买)")
    else:
        markup.add("ፍሪጅ (ለመግዛት)", "ቲቪ (ለመግዛት)")
        markup.add("ኦቭን (ለመግዛት)", "ልብስ ማጠቢያ (ለመግዛት)")
        markup.add("ውሀ ማጣሪያ (ለመግዛት)", "ቲቪ ስታንድ (ለመግዛት)")
        markup.add("የሶፋ ቴብል (ለመግዛት)")
    markup.add(get_back_button_text(lang))
    return markup

# --- 🛠️ ለማሠራት ንኡስ ሜኑ ---
def repair_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Fridge (Repair)", "TV (Repair)")
        markup.add("Oven (Repair)", "Washing Machine (Repair)")
        markup.add("Water Filter (Repair)")
    elif lang == 'om':
        markup.add("Firijii (Suphsiisuuf)", "TV (Suphsiisuuf)")
        markup.add("Oven (Suphsiisuuf)", "Maashina Uffataa (Suphsiisuuf)")
        markup.add("Calaltuu Bishaanii (Suphsiisuuf)")
    elif lang == 'ti':
        markup.add("ፍሪጅ (ንምዕራይ)", "ቲቪ (ንምዕራይ)")
        markup.add("ኦቭን (ንምዕራይ)", "ማሕጸቢ ክዳን (ንምዕራይ)")
        markup.add("ማጣሪያ ማይ (ንምዕራይ)")
    elif lang == 'so':
        markup.add("Qaboojiyaha (Dayactir)", "TV-ga (Dayactir)")
        markup.add("Oven-ka (Dayactir)", "Mashiinka Dharka (Dayactir)")
        markup.add("Sifeeyaha Biyaha (Dayactir)")
    elif lang == 'ar':
        markup.add("ثلاجة (صيانة)", "تلفزيون (صيانة)")
        markup.add("فرن (صيانة)", "غسالة ملابس (صيانة)")
        markup.add("فلتر مياه (صيانة)")
    elif lang == 'zh':
        markup.add("冰箱 (维修)", "电视 (维修)")
        markup.add("烤箱 (维修)", "洗衣机 (维修)")
        markup.add("净水器 (维修)")
    else:
        markup.add("ፍሪጅ (ለማሠራት)", "ቲቪ (ለማሠራት)")
        markup.add("ኦቭን (ለማሠራት)", "ልብስ ማጠቢያ (ለማሠራት)")
        markup.add("ውሀ ማጣሪያ (ለማሠራት)")
    markup.add(get_back_button_text(lang))
    return markup

# --- መጠኖች እና ሞዴሎች ---
def tv_size_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("32 Inch", "43 Inch", "50 Inch", "55 Inch", "65 Inch", "75 Inch")
    markup.add(get_back_button_text(lang))
    return markup

def fridge_model_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("205 Model", "310 Model", "360 Model", "400 Model", "460 Model", "560 Model")
    markup.add(get_back_button_text(lang))
    return markup

def oven_type_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("2 Gas 2 Electric Oven", "4 Electric Oven")
    markup.add(get_back_button_text(lang))
    return markup

def washing_size_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("12 KG", "13 KG", "14 KG", "15 KG", "16 KG", "18 KG", "20 KG")
    markup.add(get_back_button_text(lang))
    return markup

def table_size_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("1 Meter Table", "1.20 Meter Table")
    markup.add(get_back_button_text(lang))
    return markup

def stand_size_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("1.20 Meter Stand", "1.50 Meter Stand")
    markup.add(get_back_button_text(lang))
    return markup

# --- 🛠️ የጥገና ብልሽት ዓይነቶች ---
def fridge_repair_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Fridge - Gas", "Fridge - Bulb", "Fridge - Motor", "Fridge - Thermostat", "Fridge - Starter")
    else:
        markup.add("ፍሪጅ - ጋዝ", "ፍሪጅ - አምፓል", "ፍሪጅ - ሞተር", "ፍሪጅ - ቴርሞስታት", "ፍሪጅ - ስታርተር")
    markup.add(get_back_button_text(lang))
    return markup

def tv_repair_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("TV - Screen", "TV - Board", "TV - Backlight", "TV - Remote Sensor", "TV - T-Con Board")
    else:
        markup.add("ቲቪ - ስክሪን", "ቲቪ - ቦርድ", "ቲቪ - ባክላይት", "ቲቪ - ሪሞት ሴንሰር", "ቲቪ - ቲ-ኮን ቦርድ")
    markup.add(get_back_button_text(lang))
    return markup

def washing_repair_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Washing - Wash Motor", "Washing - Spin Motor", "Washing - Timer", "Washing - Gearbox", "Washing - Fuse")
    else:
        markup.add("ማጠቢያ - የማገቢያ ሞተር", "ማጠቢያ - የማድረቂያ ሞተር", "ማጠቢያ - ታይመር", "ማጠቢያ - ቦኮሎ", "ማጠቢያ - ፊውዝ")
    markup.add(get_back_button_text(lang))
    return markup

def oven_repair_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Oven - Plate", "Oven - Timer", "Oven - Socket", "Oven - Gas")
    else:
        markup.add("ኦቭን - ፕሌት", "ኦቭን - ታይመር", "ኦቭን - ሶኬት", "ኦቭን - ጋዝ")
    markup.add(get_back_button_text(lang))
    return markup

def filter_repair_keyboard(lang='am'):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if lang == 'en':
        markup.add("Filter - Hot Water", "Filter - Cold Water", "Filter - Sand Filter")
    else:
        markup.add("ማጣሪያ - ሙቅ", "ማጣሪያ - ቀዝቃዛ", "ማጣሪያ - አሸዋ")
    markup.add(get_back_button_text(lang))
    return markup

# 📊 /count - የተጠቃሚዎች ብዛት ማወቂያ ትዕዛዝ
@bot.message_handler(commands=['count'])
def count_users(message):
    if message.from_user.id != MY_ADMIN_ID:
        bot.send_message(message.chat.id, "❌ ይህንን ትዕዛዝ የመጠቀም መብት የለዎትም።")
        return

    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
        total_users = len(users)
        bot.send_message(MY_ADMIN_ID, f"📊 **እስካሁን ቦቱን የጀመሩ (Start ያሉ) ጠቅላላ ተጠቃሚዎች ብዛት፦** `{total_users}` ሰዎች ናቸው።", parse_mode="Markdown")
    else:
        bot.send_message(MY_ADMIN_ID, "❌ እስካሁን ምንም የተመዘገበ ተጠቃሚ የለም።")

# 📢 /broadcast - የጅምላ መልእክት መላኪያ ትዕዛዝ
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != MY_ADMIN_ID:
        bot.send_message(message.chat.id, "❌ ይህንን ትዕዛዝ የመጠቀም መብት የለዎትም።")
        return

    msg_text = message.text.replace("/broadcast", "").strip()
    if not msg_text:
        bot.send_message(message.chat.id, "⚠️ **እባክዎን የሚላከውን መልእክት አብረው ይጻፉ!**\n\nምሳሌ፦ `/broadcast ሰላም አዳዲስ እቃዎች ገብተዋል!`", parse_mode="Markdown")
        return

    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
        
        count = 0
        for u_id in users:
            try:
                bot.send_message(u_id, msg_text)
                count += 1
            except Exception:
                pass
        
        bot.send_message(MY_ADMIN_ID, f"✅ መልእክቱ ለ **{count}** ተጠቃሚዎች በተሳካ ሁኔታ ተልኳል!")
    else:
        bot.send_message(MY_ADMIN_ID, "❌ እስካሁን ምንም የተመዘገበ ተጠቃሚ የለም።")

# /start ሲባል ቋንቋ ያስመርጣል
@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id)
    user_states[message.chat.id] = None
    welcome_text = (
        "ሰላም! Welcome to Daniel Electronics Repair! 👋\n\n"
        "እባክዎን ቋንቋ ይምረጡ / Please select your language:\n"
        "Maaloo afaan filadhaa / ቋንቋኹም ሕረዩ / Dooro Luqadda / اختر اللغة / 请选择语言"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=language_keyboard())

# 📷 ፎቶ ተቀባይ (ለዋስትና ደረሰኝ ፎቶ)
@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    chat_id = message.chat.id
    user = message.from_user
    username_text = f"@{user.username}" if user.username else "የለውም"
    lang = user_language.get(chat_id, 'am')

    if user_states.get(chat_id) == "waiting_for_warranty_receipt":
        user_states[chat_id] = None
        item_info = user_warranty_item.get(chat_id, "እቃ")
        desc_info = user_warranty_desc.get(chat_id, "ገለጻ የለም")
        photo_file_id = message.photo[-1].file_id

        thanks_msg = "እናመሰግናለን! የዋስትና ጥያቄዎ እና የደረሰኝ ፎቶ ደርሶናል፤ አረጋግጠን በቅርቡ እንመላስልዎታለን። 🙏"
        bot.send_message(chat_id, thanks_msg, reply_markup=main_keyboard(lang))

        admin_caption = (
            f"🛡️ **አዲስ የዋስትና አገልግሎት ጥያቄ!**\n\n"
            f"👤 **ደንበኛ:** [{user.first_name}](tg://user?id={user.id})\n"
            f"USERNAME: {username_text}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"📦 **የተመረጠው እቃ:** {item_info}\n"
            f"📝 **የብልሽት/ችግር መግለጫ:** {desc_info}"
        )
        try:
            bot.send_photo(MY_ADMIN_ID, photo_file_id, caption=admin_caption, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(MY_ADMIN_ID, f"⚠️ ፎቶውን ወደ አድሚን መላክ አልተቻለም: {e}")
        return

    bot.send_message(chat_id, "📷 ፎቶዎ ደርሶናል! ግን እባክዎን ከዋስትና ውጪ ለሌላ ነገር ፎቶ ከመላክዎ በፊት ተዛማጅ ሜኑዎችን ይጠቀሙ።")

# የደንበኞች መልእክቶች ማስተናገጃ
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    save_user(message.chat.id)
    text = message.text
    user = message.from_user
    chat_id = message.chat.id
    username_text = f"@{user.username}" if user.username else "የለውም"
    
    lang = user_language.get(chat_id, 'am')
    back_menus = ["⬅️ ወደ ዋና ሜኑ", "⬅️ Back to Main Menu", "⬅️ Gara Menu Guddaatti", "⬅️ ናብ ዋና ሜኑ ምለስ", "⬅️ Ku Noqo Liiska Weyn", "⬅️ العودة إلى القائمة الرئيسية", "⬅️ 返回主菜单", "🛒 ወደ ዋና ሜኑ"]

    # ቋንቋ ሲመረጥ
    if text == "🇪🇹 አማርኛ":
        user_language[chat_id] = 'am'
        bot.send_message(chat_id, "እንኳን ወደ Daniel Electronics Repair በደህና መጡ! 👋\nከታች ያሉትን አማራጮች ይጠቀሙ።", reply_markup=main_keyboard('am'))
        return
    elif text == "🇬🇧 English":
        user_language[chat_id] = 'en'
        bot.send_message(chat_id, "Welcome to Daniel Electronics Repair! 👋\nPlease choose an option below.", reply_markup=main_keyboard('en'))
        return
    elif text == "🌳 Afaan Oromoo":
        user_language[chat_id] = 'om'
        bot.send_message(chat_id, "Baga gara Daniel Electronics Repair nagaan dhuftan! 👋\nFilannoowwan gadii fayyadamaa.", reply_markup=main_keyboard('om'))
        return
    elif text == "🇪🇷 ትግርኛ":
        user_language[chat_id] = 'ti'
        bot.send_message(chat_id, "ብደሓን መጻእኩም ናብ ዳንኤል ኤሌክትሮኒክስ ጥገና! 👋\nብኸምዚ ኣብ ታሕቲ ዘሎ መማረጺ ተጠቐሙ።", reply_markup=main_keyboard('ti'))
        return
    elif text == "🇸🇴 Soomaaliga":
        user_language[chat_id] = 'so'
        bot.send_message(chat_id, "Ku soo dhawoow Daniel Electronics Repair! 👋\nFadlan dooro ikhtiyaarka hoose.", reply_markup=main_keyboard('so'))
        return
    elif text == "🇸🇦 العربية":
        user_language[chat_id] = 'ar'
        bot.send_message(chat_id, "مرحباً بك في صيانة الأجهزة الإلكترونية دانيال! 👋\nيرجى اختيار أحد الخيارات أدناه.", reply_markup=main_keyboard('ar'))
        return
    elif text == "🇨🇳 中文":
        user_language[chat_id] = 'zh'
        bot.send_message(chat_id, "欢迎来到丹尼尔电子维修！ 👋\n请选择以下选项。", reply_markup=main_keyboard('zh'))
        return

    # 1. የዋስትና ብልሽት መግለጫ ሲጻፍ
    if user_states.get(chat_id) == "waiting_for_warranty_desc" and text not in back_menus:
        user_warranty_desc[chat_id] = text
        user_states[chat_id] = "waiting_for_warranty_receipt"
        bot.send_message(chat_id, "📸 እጅግ በጣም እናመሰግናለን! አሁን ደግሞ **የገዙበትን ደረሰኝ (Receipt) ፎቶ** 📷 ልኮልን ይላኩ።", parse_mode="Markdown")
        return

    # 2. ለማማከር በጀት ሲጻፍ
    if user_states.get(chat_id) == "waiting_for_consult_budget" and text not in back_menus:
        user_states[chat_id] = None
        selected_item_info = user_consult_item.get(chat_id, "እቃ")
        
        thanks_msg = "እናመሰግናለን! የማማከር ጥያቄዎ፣ የእቃው ዝርዝር እና የበጀት መጠንዎ ደርሶናል፤ በቅርቡ ደውለን እናናግርዎታለን! 🙏"
        bot.send_message(chat_id, thanks_msg, reply_markup=main_keyboard(lang))

        admin_notification = (
            f"💡 **አዲስ የማማከር ጥያቄ ከደንበኛ!**\n\n"
            f"👤 **ደንበኛ:** [{user.first_name}](tg://user?id={user.id})\n"
            f"USERNAME: {username_text}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"📦 **የተመረጠው እቃ እና መጠን/ሞዴል:** {selected_item_info}\n"
            f"💰 **የተመደበ በጀት እና ስልክ:** {text}"
        )
        try:
            bot.send_message(MY_ADMIN_ID, admin_notification, parse_mode="Markdown")
        except Exception:
            pass
        return

    # 3. አስተያየት ሲጻፍ
    if user_states.get(chat_id) == "waiting_for_feedback" and text not in back_menus:
        user_states[chat_id] = None
        thanks_msg = "ለአስተያየትዎ እናመሰግናለን! 🙏"
        bot.send_message(chat_id, thanks_msg, reply_markup=main_keyboard(lang))

        admin_notification = (
            f"💬 **አዲስ አስተያየት ከደንበኛ!**\n\n"
            f"👤 **ደንበኛ:** [{user.first_name}](tg://user?id={user.id})\n"
            f"USERNAME: {username_text}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"📝 **አስተያየት:** {text}"
        )
        try:
            bot.send_message(MY_ADMIN_ID, admin_notification, parse_mode="Markdown")
        except Exception:
            pass
        return

    # --- ዋና ሜኑዎች ---
    if text in ["🛒 ዕቃ ለመግዛት", "🛒 Shop", "🛒 Meeshaa Bitachuuf", "🛒 ንግዛእ ንብረት", "🛒 Iibsashada Alaabta", "🛒 شراء البضائع", "🛒 购买商品"]:
        user_states[chat_id] = None
        bot.send_message(chat_id, "🛒 **ለመግዛት የሚፈልጉትን ዕቃ ይምረጡ፡**", parse_mode="Markdown", reply_markup=buy_keyboard(lang))

    elif text in ["🛠️ ዕቃ ለማሠራት", "🛠️ Maintenance", "🛠️ Meeshaa Suphsiisuuf", "🛠️ ንብረት ንምዕራይ", "🛠️ Dayactirka Alaabta", "🛠️ صيانة الأجهزة", "🛠️ 设备维修"]:
        user_states[chat_id] = None
        bot.send_message(chat_id, "🛠️ **ለማሠራት/ለመጠገን የሚፈልጉትን ዕቃ ይምረጡ፡**", parse_mode="Markdown", reply_markup=repair_keyboard(lang))

    elif text in ["🛡️ የዋስትና አገልግሎት", "🛡️ Warranty Service", "🛡️ Tajaajila Wabii (Warranty)", "🛡️ ኣገልግሎት ውሕስና (Warranty)", "🛡️ Adeegga Damaanadda", "🛡️ خدمة الضمان", "🛡️ 保修服务"]:
        user_states[chat_id] = None
        bot.send_message(chat_id, "🛡️ **እባክዎን የዋስትና አገልግሎት የሚፈልጉትን የተበላሸ እቃ ይምረጡ፡**", parse_mode="Markdown", reply_markup=warranty_item_keyboard(lang))

    elif text in ["📞 ለማማከር", "📞 Consultation", "📞 Mari'achuuf", "📞 ምኽሪ ንግበር", "📞 La Tashiga", "📞 الاستشارة", "📞 咨询服务"]:
        user_states[chat_id] = None
        bot.send_message(chat_id, "📞 **ሊገዙ ያሰቡትን እና ሊማከሩበት የሚፈልጉትን እቃ ይምረጡ፡**", parse_mode="Markdown", reply_markup=consult_keyboard(lang))

    elif text in ["📦 እቃ ለመምረጥ", "📦 Choose Items", "📦 Meeshaa Filachuuf", "📦 ንብረት ንምረጽ", "📦 Dooro Alaabta", "📦 اختر العناصر", "📦 选择商品"]:
        user_states[chat_id] = None
        markup_channel = types.InlineKeyboardMarkup()
        btn_channel = types.InlineKeyboardButton("🔗 ቻናላችንን ለመቀላቀል (Join)", url="https://t.me/dani_tech15")
        markup_channel.add(btn_channel)
        bot.send_message(chat_id, "📦 **እቃዎችን ለመምረጥ እና ቀጥታ ለመመልከት ከታች ያለውን ሊንክ በመጫን ቻናላችንን join ይበሉ!** 👉 @dani_tech15", reply_markup=markup_channel)

    elif text in back_menus:
        user_states[chat_id] = None
        bot.send_message(chat_id, "ወደ ዋናው ሜኑ ተመልሰዋል፡", reply_markup=main_keyboard(lang))

    elif text in ["🌐 ቋንቋ ለመቀየር", "🌐 Change Language", "🌐 Afaan Jijjiiruuf", "🌐 ቋንቋ ንምቕያር", "🌐 Beddel Luqadda", "🌐 تغير اللغات", "🌐 更改语言"]:
        bot.send_message(chat_id, "እባክዎን ቋንቋ ይምረጡ / Please select your language:", reply_markup=language_keyboard())

    elif text in ["💬 አስተያየት", "💬 Feedback", "💬 Yaada", "💬 ርእይቶ", "💬 Ra'yigaaga", "💬 ملاحظاتك", "💬 用户反馈"]:
        user_states[chat_id] = "waiting_for_feedback"
        bot.send_message(chat_id, "✍️ **እባክዎን አስተያየትዎን ወይም ጥያቄዎን እዚህ ይጻፉልን፦**", parse_mode="Markdown")

    elif text in ["🛠️ አገልግሎቶች", "🛠️ Services", "🛠️ Tajaajiloota", "🛠️ ኣገልግሎታት", "🛠️ Adeegyada", "🛠️ الخدمات", "🛠️ 我们的服务"]:
        user_states[chat_id] = None
        response = (
            "እኛ የምንሰጣቸው አገልግሎቶች፦\n"
            "• 🧊 የፍሪጅ ሸያጭ እና ጥገና\n"
            "• 📺 የቲቪ (TV) ሸያጭ እና ጥገና ከ 32 inch እስከ 75 inch\n"
            "• 📻 የሬሲቨር ጥገና እና አክሰሰሪ ሸያጭ\n"
            "• 🧺 የልብስ ማጠቢያ ሸያጭ እና ጥገና\n"
            "• 🚰 የውሃ ማጣሪያ ሸያጭ እና ጥገና\n"
            "• ⚡ እና የሌሎች የኤሌክትሮኒክ እቃዎች ጥገና አገልግሎት እንሰጣለን።\n\n"
            "✅ ከበቂ መለዋወጫ አክሰሰሪዎች ከ 1 ዓመት ዋስትና ጋር!\n\n"
            "ለበለጠ መረጃ 👉 @dani_tech16 ይጠቀሙ።"
        )
        bot.send_message(chat_id, response, reply_markup=main_keyboard(lang))

    elif text in ["📞 ስልክ ቁጥር", "📞 Phone", "📞 Lakkoofsa Bilbilaa", "📞 ቁጽሪ ስልኪ", "📞 Lambarka Taleefanka", "📞 رقم الهاتف", "📞 电话号码"]:
        user_states[chat_id] = None
        response = "📞 በ 0918845007 ወይም በ 0718845007 ይደውሉልን!\nማንኛውም ማህበራዊ ሚዲያ ላይ 👉 @dani_tech16 ያገኙናል።"
        bot.send_message(chat_id, response, reply_markup=main_keyboard(lang))

    elif text in ["📍 አድራሻ", "📍 Location", "📍 Teessoo", "📍 ኣድራሻ", "📍 Goobta", "📍 الموقع", "📍 地址"]:
        user_states[chat_id] = None
        response = "📍 አድራሻችን፦ ሳሪስ አደይ አበባ ኮቴክስ ቲሸርት ጎን 3F ከፍ ብሎ (ዳንኤል ኤሌክትሮኒክስ) የሽያጭ ሰዓት ከ ሰኞ እስከ ቅዳሜ ከጠዋቱ 2:00 እስከ ምሽቱ 2:00 ለጥገና አገልግሎት 24/7 ይደውሉ"
        bot.send_message(chat_id, response, reply_markup=main_keyboard(lang))

    # --- 🛡️ የዋስትና እቃ ሲመረጥ ---
    elif text in ["ፍሪጅ (ዋስትና)", "Fridge (Warranty)", "ቲቪ (ዋስትና)", "TV (Warranty)", "ኦቭን (ዋስትና)", "Oven (Warranty)", "ልብስ ማጠቢያ (ዋስትና)", "Washing Machine (Warranty)", "ውሀ ማጣሪያ (ዋስትና)", "Water Filter (Warranty)", "ቲቪ ስታንድ (ዋስትና)", "TV Stand (Warranty)", "የሶፋ ቴብል (ዋስትና)", "Sofa Table (Warranty)"]:
        user_warranty_item[chat_id] = text
        user_states[chat_id] = "waiting_for_warranty_desc"
        bot.send_message(chat_id, f"📝 እቃው **{text}** ተመርጧል።\n\nእባክዎን እቃው ላይ ያጋጠመውን **ችግር ወይም ብልሽት (ምን እንደሆነ) በጽሁፍ** በዝርዝር ይጻፉልን፦", parse_mode="Markdown")

    # --- 💡 ለማማከር እቃ ሲመረጥ ---
    elif text in ["ቲቪ (ለማማከር)", "TV (Consult)", "TV (Mari'achuuf)", "ቲቪ (ምኽሪ)", "TV-ga (La Tashi')", "تلفزيون (استشارة)", "电视咨询"]:
        user_consult_item[chat_id] = "ቲቪ (ለማማከር)"
        bot.send_message(chat_id, "📺 **የሚፈልጉትን የቲቪ (TV) መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=tv_size_keyboard(lang))

    elif text in ["ፍሪጅ (ለማማከር)", "Fridge (Consult)", "Firijii (Mari'achuuf)", "ፍሪጅ (ምኽሪ)", "Qaboojiyaha (La Tashi')", "ثلاجة (استشارة)", "冰箱咨询"]:
        user_consult_item[chat_id] = "ፍሪጅ (ለማማከር)"
        bot.send_message(chat_id, "🧊 **የሚፈልጉትን የፍሪጅ ሞዴል ይምረጡ፡**", parse_mode="Markdown", reply_markup=fridge_model_keyboard(lang))

    elif text in ["ኦቭን (ለማማከር)", "Oven (Consult)", "Oven (Mari'achuuf)", "ኦቭን (ምኽሪ)", "Oven-ka (La Tashi')", "فرن (استشارة)", "烤箱咨询"]:
        user_consult_item[chat_id] = "ኦቭን (ለማማከር)"
        bot.send_message(chat_id, "🍳 **የሚፈልጉትን የኦቭን ዓይነት ይምረጡ፡**", parse_mode="Markdown", reply_markup=oven_type_keyboard(lang))

    elif text in ["ልብስ ማጠቢያ (ለማማከር)", "Washing Machine (Consult)", "Maashina Uffataa (Mari'achuuf)", "ማሕጸቢ ክዳን (ምኽሪ)", "Mashiinka Dharka (La Tashi')", "غسالة ملابس (استشارة)", "洗衣机咨询"]:
        user_consult_item[chat_id] = "ልብስ ማጠቢያ (ለማማከር)"
        bot.send_message(chat_id, "🧺 **የሚፈልጉትን የልብስ ማጠቢያ መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=washing_size_keyboard(lang))

    elif text in ["የሶፋ ቴብል (ለማማከር)", "Sofa Table (Consult)", "Minoo Soofaa (Mari'achuuf)", "ሶፋ ጠረጴዛ (ምኽሪ)", "Miiska Fadhiga (La Tashi')", "طاولة صوفا (استشارة)", "沙发桌咨询"]:
        user_consult_item[chat_id] = "የሶፋ ቴብል (ለማማከር)"
        bot.send_message(chat_id, "🛋️ **የሚፈልጉትን የሶፋ ቴብል መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=table_size_keyboard(lang))

    elif text in ["ቲቪ ስታንድ (ለማማከር)", "TV Stand (Consult)", "TV Stand (Mari'achuuf)", "ቲቪ ስታንድ (ምኽሪ)", "TV Stand (La Tashi')", "حامل تلفزيون (استشارة)", "电视柜咨询"]:
        user_consult_item[chat_id] = "ቲቪ ስታንድ (ለማማከር)"
        bot.send_message(chat_id, "📺 **የሚፈልጉትን የቲቪ ስታንድ መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=stand_size_keyboard(lang))

    # ደንበኛው የማማከር እቃ መጠን/ሞዴል ከመረጠ በኋላ በጀት ሲጠየቅ
    elif any(k in text for k in ["Inch", "Model", "Table", "Stand", "KG", "Oven", "ኢንች", "ሞዴል", "ቴብል", "ስታንድ", "ኪሎ"]):
        if user_consult_item.get(chat_id):
            user_states[chat_id] = "waiting_for_consult_budget"
            user_consult_item[chat_id] = f"{user_consult_item.get(chat_id)} - {text}"
            bot.send_message(chat_id, "💰 **እባክዎን የሚመድቡትን የበጀት መጠን (ስንት ብር ማውጣት እንደሚፈልጉ) እና ስልክ ቁጥርዎን እዚህ ይጻፉልን፦**", parse_mode="Markdown")
        else:
            user_states[chat_id] = None
            item_name = text
            response = f"🛒 **የ{item_name} ግዢ ጥያቄዎ ደርሶናል!**\n\n📍 **አድራሻችን፦** ሳሪስ አደይ አበባ ኮቴክስ ቲሸርት ጎን 3F\n📞 **በቀጥታ ለመደወል፦** 0918845007 / 0718845007\n\n✍️ እባክዎን ስልክ ቁጥርዎን እዚህ ይጻፉልን።"
            bot.send_message(chat_id, response)

            admin_notification = f"🛒 **አዲስ የግዢ ፍላጎት!**\n\n👤 **ደንበኛ:** [{user.first_name}](tg://user?id={user.id})\nUSERNAME: {username_text}\n🆔 **ID:** `{user.id}`\n📦 **የመረጡት ዕቃ:** {item_name}"
            try:
                bot.send_message(MY_ADMIN_ID, admin_notification, parse_mode="Markdown")
            except Exception:
                pass

    # --- 🛠️ የጥገና ንኡስ ሜኑዎች ---
    elif text in ["ፍሪጅ (ለማሠራት)", "Fridge (Repair)", "Firijii (Suphsiisuuf)", "ፍሪጅ (ንምዕራይ)", "Qaboojiyaha (Dayactir)", "ثلاجة (صيانة)", "冰箱 (维修)"]:
        bot.send_message(chat_id, "🧊 **የፍሪጁን የብልሽት ዓይነት ይምረጡ፡**", parse_mode="Markdown", reply_markup=fridge_repair_keyboard(lang))

    elif text in ["ቲቪ (ለማሠራት)", "TV (Repair)", "TV (Suphsiisuuf)", "ቲቪ (ንምዕራይ)", "TV-ga (Dayactir)", "تلفزيون (صيانة)", "电视 (维修)"]:
        bot.send_message(chat_id, "📺 **የቲቪውን የብልሽት ዓይነት ይምረጡ፡**", parse_mode="Markdown", reply_markup=tv_repair_keyboard(lang))

    elif text in ["ልብስ ማጠቢያ (ለማሠራት)", "Washing Machine (Repair)", "Maashina Uffataa (Suphsiisuuf)", "ማሕጸቢ (ንምዕራይ)", "Mashiinka Dharka (Dayactir)", "غسالة ملابس (صيانة)", "洗衣机 (维修)"]:
        bot.send_message(chat_id, "🧺 **የልብስ ማጠቢያውን የብልሽት ዓይነት ይምረጡ፡**", parse_mode="Markdown", reply_markup=washing_repair_keyboard(lang))

    elif text in ["ኦቭን (ለማሠራት)", "Oven (Repair)", "Oven (Suphsiisuuf)", "ኦቭን (ንምዕራይ)", "Oven-ka (Dayactir)", "فرن (صيانة)", "烤箱 (维修)"]:
        bot.send_message(chat_id, "🍳 **የኦቭኑን የብልሽት ዓይነት ይምረጡ፡**", parse_mode="Markdown", reply_markup=oven_repair_keyboard(lang))

    elif text in ["ውሀ ማጣሪያ (ለማሠራት)", "Water Filter (Repair)", "Calaltuu Bishaanii (Suphsiisuuf)", "ማጣሪያ ማይ (ንምዕራይ)", "Sifeeyaha Biyaha (Dayactir)", "فلتر مياه (صيانة)", "净水器 (维修)"]:
        bot.send_message(chat_id, "🚰 **የውሃ ማጣሪያውን የብልሽት ዓይነት ይምረጡ፡**", parse_mode="Markdown", reply_markup=filter_repair_keyboard(lang))

    # --- 🛒 የግዢ ንኡስ ሜኑዎች ---
    elif text in ["ቲቪ (ለመግዛት)", "TV (Buy)", "TV (Bitachuuf)", "ቲቪ (ንግዛእ)", "TV-ga (Iibso)", "تلفزيون (شراء)", "电视 (购买)"]:
        bot.send_message(chat_id, "📺 **የሚፈልጉትን የቲቪ (TV) መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=tv_size_keyboard(lang))

    elif text in ["ፍሪጅ (ለመግዛት)", "Fridge (Buy)", "Firijii (Bitachuuf)", "ፍሪጅ (ንግዛእ)", "Qaboojiyaha (Iibso)", "ثلاجة (شراء)", "冰箱 (购买)"]:
        bot.send_message(chat_id, "🧊 **የሚፈልጉትን የፍሪጅ ሞዴል ይምረጡ፡**", parse_mode="Markdown", reply_markup=fridge_model_keyboard(lang))

    elif text in ["ኦቭን (ለመግዛት)", "Oven (Buy)", "Oven (Bitachuuf)", "ኦቭን (ንግዛእ)", "Oven-ka (Iibso)", "فرن (شراء)", "烤箱 (购买)"]:
        bot.send_message(chat_id, "🍳 **የሚፈልጉትን የኦቭን ዓይነት ይምረጡ፡**", parse_mode="Markdown", reply_markup=oven_type_keyboard(lang))

    elif text in ["ልብስ ማጠቢያ (ለመግዛት)", "Washing Machine (Buy)", "Maashina Uffataa (Bitachuuf)", "ማሕጸቢ ክዳን (ንግዛእ)", "Mashiinka Dharka (Iibso)", "غسالة ملابس (شراء)", "洗衣机 (购买)"]:
        bot.send_message(chat_id, "🧺 **የሚፈልጉትን የልብስ ማጠቢያ መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=washing_size_keyboard(lang))

    elif text in ["የሶፋ ቴብል (ለመግዛት)", "Sofa Table (Buy)", "Minoo Soofaa (Bitachuuf)", "ሶፋ ጠረጴዛ (ንግዛእ)", "Miiska Fadhiga (Iibso)", "طاولة صوفا (شراء)", "沙发桌 (购买)"]:
        bot.send_message(chat_id, "🛋️ **የሚፈልጉትን የሶፋ ቴብል መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=table_size_keyboard(lang))

    elif text in ["ቲቪ ስታንድ (ለመግዛት)", "TV Stand (Buy)", "TV Stand (Bitachuuf)", "ቲቪ ስታንድ (ንግዛእ)", "TV Stand (Iibso)", "حامل تلفزيون (شراء)", "电视柜 (购买)"]:
        bot.send_message(chat_id, "📺 **የሚፈልጉትን የቲቪ ስታንድ መጠን ይምረጡ፡**", parse_mode="Markdown", reply_markup=stand_size_keyboard(lang))

    # የጥገና ብልሽት ዓይነት ሲመረጥ
    elif any(p in text for p in ["ፍሪጅ -", "ቲቪ -", "ማጠቢያ -", "ኦቭን -", "ማጣሪያ -"]):
        user_states[chat_id] = None
        response = f"🛠️ **የ{text} ጥገና ጥያቄዎ ደርሶናል!**\n\n📞 **በቀጥታ ለመደወል፦** 0918845007 / 0718845007\n\n✍️ እባክዎን ስልክ ቁጥርዎን እዚህ ይጻፉልን፤ ቴክኒሽያኑ ይደውልልዎታል።"
        bot.send_message(chat_id, response)

        admin_notification = f"🛠️ **አዲስ የጥገና ጥያቄ!**\n\n👤 **ደንበኛ:** [{user.first_name}](tg://user?id={user.id})\nUSERNAME: {username_text}\n🆔 **ID:** `{user.id}`\n🔧 **የተመረጠው ብልሽት:** {text}"
        try:
            bot.send_message(MY_ADMIN_ID, admin_notification, parse_mode="Markdown")
        except Exception:
            pass

    # ደንበኛው ስልኩን ወይም መልእክት ሲፅፍ
    else:
        user_states[chat_id] = None
        thanks_reply = "እናመሰግናለን! የጻፉልን መረጃ ደርሶናል፤ በቅርቡ ደውለን እናናግርዎታለን።"
        bot.send_message(chat_id, thanks_reply)

        admin_notification = f"📩 **አዲስ መልእክት/ስልክ ከደንበኛ!**\n\n👤 **ደንበኛ:** [{user.first_name}](tg://user?id={user.id})\nUSERNAME: {username_text}\n🆔 **ID:** `{user.id}`\n💬 **መልእክት:** {text}"
        try:
            bot.send_message(MY_ADMIN_ID, admin_notification, parse_mode="Markdown")
        except Exception:
            pass

bot.polling(non_stop=True, timeout=60, long_polling_timeout=60)
