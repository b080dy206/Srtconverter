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
            srt_text += f"{index}\n{line.replace('.', ',')}\n"  # تغيير النقطة إلى فاصلة
            index += 1
        else:
            # إضافة الترجمة
            srt_text += f"{line}\n"
    
    return srt_text

# استقبال النصوص وتحويلها إلى SRT
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    webvtt_text = message.text
    
    # تحويل WEBVTT إلى SRT
    srt_content = webvtt_to_srt(webvtt_text)
    
    # حفظ الملف SRT
    with open("converted_subtitles.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)
    
    # إرسال الملف SRT للمستخدم
    with open("converted_subtitles.srt", "rb") as f:
        bot.send_document(message.chat.id, f, caption="📂 إليك ملف SRT المحول")

# تشغيل البوت
bot.polling()
