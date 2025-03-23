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

# دالة لتحويل ملف SRT إلى نص
def srt_to_text(file):
    subs = srt.parse(file)
    text = "\n".join([sub.content for sub in subs])
    return text

# استقبال النصوص وتحويلها إلى ملف SRT
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    text = message.text
    srt_content = text_to_srt(text)
    with open("subtitles.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    with open("subtitles.srt", "rb") as f:
        bot.send_document(message.chat.id, f, caption="📂 إليك ملف SRT الخاص بك!")

# استقبال ملفات SRT وتحويلها إلى نص
@bot.message_handler(content_types=['document'])
def handle_file(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    
    # تحويل ملف SRT إلى نص
    text = srt_to_text(file.decode('utf-8'))
    
    # إرسال النص للمستخدم
    bot.send_message(message.chat.id, f"تم تحويل ملف SRT إلى نص:\n{text}")

# تشغيل البوت
bot.polling()
