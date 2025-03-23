import telebot
import re

# ضع توكن البوت هنا
TOKEN = "7943071605:AAEAoBMvRqov32mDJoaptjEhPnHnf5XcCAM"
bot = telebot.TeleBot(TOKEN)

# دالة لتحويل WEBVTT إلى SRT
def webvtt_to_srt(webvtt_text):
    # إزالة أي رأس للملف WEBVTT
    webvtt_text = re.sub(r"^WEBVTT.*\n", "", webvtt_text)
    
    # تحويل النص إلى تنسيق SRT
    srt_text = ""
    lines = webvtt_text.splitlines()
    index = 1
    for line in lines:
        if "-->" in line:
            # إضافة التوقيت
            srt_text += f"{index}\n{line}\n"
            index += 1
        else:
            # إضافة الترجمة
            srt_text += f"{line}\n"
    
    return srt_text

# استقبال ملفات WEBVTT وتحويلها إلى SRT
@bot.message_handler(content_types=['document'])
def handle_file(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    
    # تحويل WEBVTT إلى SRT
    srt_content = webvtt_to_srt(file.decode('utf-8'))
    
    # حفظ الملف SRT
    with open("converted_subtitles.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    # إرسال الملف SRT للمستخدم
    with open("converted_subtitles.srt", "rb") as f:
        bot.send_document(message.chat.id, f, caption="📂 إليك ملف SRT المحول")

# تشغيل البوت
bot.polling()
