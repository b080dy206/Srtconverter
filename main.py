import telebot  
import srt  
from datetime import timedelta  

# ضع توكن البوت هنا
TOKEN = "7943071605:AAEAoBMvRqov32mDJoaptjEhPnHnf5XcCAM"  
bot = telebot.TeleBot(TOKEN)

# دالة لتحويل النص إلى SRT
def text_to_srt(text):
    lines = text.strip().split("\n")  # تقسيم النص إلى أسطر
    subtitles = []
    for i, line in enumerate(lines):
        start_time = timedelta(seconds=i * 2)  # كل جملة تبدأ بعد 2 ثانية
        end_time = start_time + timedelta(seconds=2)  # مدة العرض 2 ثانية
        subtitles.append(srt.Subtitle(index=i + 1, start=start_time, end=end_time, content=line))
    return srt.compose(subtitles)

# استقبال النصوص وتحويلها إلى ملف SRT
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    srt_content = text_to_srt(text)
    with open("subtitles.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)

    with open("subtitles.srt", "rb") as f:
        bot.send_document(message.chat.id, f, caption="📂 إليك ملف SRT الخاص بك!")

# تشغيل البوت
bot.polling()