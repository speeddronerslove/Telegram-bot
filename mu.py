import random
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from fuzzywuzzy import process  # For fuzzy matching (install with `pip install fuzzywuzzy`)

# ✅ Replace with your free DeepInfra API Key
FREE_AI_API_KEY = "Rns7MsYfbCmOvckyFbBRTvhFvWb44UTp"
BOT_TOKEN = "5242900497:AAFScAueV_Z2WBYORY25o_wubim4qIgV5jE"

# ✅ Manually define chat data
chat_data = {
    "saaptiya?": ["Sapten da! Nee? 😄", "Illada innum late aagum", "saapdalaam porumaiyah nee sollu", "saaptutene yeppavoh"],
    "Hi da!": ["Haha! solludaa 😂","Solra Punda","Yenna vishayam maamey","Yennachu bro","sollu pa","YEnnachu "],
    "enna da plan?": ["Onnum illa bro, unaku irundha sollu? 🤔"],
    "sapten da": ["Seri Seri yenna saapta 🍔","Seri sootha moodiko","adhuku yenna ippo","Nalladhu"],
    "Thevdiya": ["Gommala Ketta vaartha use panna sootha kilichi kaaya poturuven da potta 🤣🔥","Adha oru Thevdiya munda solludhu"],
    "potta": ["Gommala Ketta vaartha use panna sootha kilichi kaaya poturuven da potta 🔥","Neethan da potta poruki"],
    "Punda": ["Gommala Ketta vaartha use panna sootha kilichi kaaya poturuven da potta 😜","Yaaru punda undha"],
    "kuthi": ["Gommala Ketta vaartha use panna sootha kilichi kaaya poturuven da potta 💥","Adhellam unaku irukum da"],
    "poolu": ["Gommala Ketta vaartha use panna sootha kilichi kaaya poturuven da potta 🌸","Yenna poolu swimming poolu ah"],
    "oombu": ["Gommala Ketta vaartha use panna sootha kilichi kaaya poturuven da potta 🌪️","Yedhuthu veliya vidu oombuvoom"],
    "dei": ["solleh 👀","solra","Yennachu","Ahaan!!!","sollupa"],
    "Apparam yenna pannituruka": ["Yenna pathi theriyaadha ... non chat bot uh Backend run aagura vara run aaguven 💻⚡"],
    "oh ho": ["Aaama pa 😏"],
    "Mogana murali yenga": ["Avaru Offline or yedachum work la irupaaru pa 🧑‍💻"],
    "yaaru unna create panna": ["murali dhaan 👨‍💻"],
    "Yenna panra": ["Summa dhaan unaku reply pannuturuken"],
    "Macha": ["Solra macha"],
    "Boring ah iruku da": ["Poi padi da"],
    "seri": ["Haan da pesa content illayah"],
    "ajay": ["Ajay nalla paiyan da"],
}

# ✅ Load Custom Chat Data from JSON (Now defined manually)
def get_custom_reply(user_message):
    """Check predefined chat data for the closest matching response using fuzzy matching."""
    try:
        # Get the closest match (threshold 80% similarity)
        best_match, score = process.extractOne(user_message, chat_data.keys())
        if score > 80:
            response = chat_data[best_match]
            return random.choice(response) if isinstance(response, list) else response  # ✅ Fix: Random choice for lists
    except Exception as e:
        print(f"Error in fuzzy matching: {e}")
    
    return None

# ✅ Function to Get AI Reply Using Free GPT-3.5 API
def get_ai_reply(user_message):
    """First check manual chat data with fuzzy matching, then call AI if no match."""
    custom_reply = get_custom_reply(user_message)
    if custom_reply:
        return custom_reply  # If matched, return predefined response.

    try:
        response = requests.post(
            "https://api.deepinfra.com/v1/openai/chat/completions",
            json={
                "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                "messages": [
                    {"role": "system", "content": (
                        "Nee oru Tamil Tanglish chatbot da! Pesum style Tamil la irukkanum, "
                        "aana English alphabets la dhan type pannum. **Tamil slang maintain pannu!** "
                        "Reply casual ah irukkanum, like local chat. Short ah pesu, emoji use pannu!"
                    )},
                    {"role": "user", "content": user_message},
                ],
            },
            headers={"Authorization": f"Bearer {FREE_AI_API_KEY}"},
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error with Free AI API: {e}")
        return "Sorry da, enakku puriyala. olunga sollu  bro!"

# ✅ Function to Handle Messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    """Reply using AI-generated responses."""
    user_message = update.message.text
    reply = get_ai_reply(user_message)
    await update.message.reply_text(reply)

# ✅ Start Command
async def start(update: Update, context: CallbackContext) -> None:
    """Start command with Branding."""
    await update.message.reply_text(
        "🔥 Vanakkam da! Naan unga AI assistant, **MoganaMurali's Bot**! 😎\n"
        "Tanglish pesunga, naan reply pannuren! 💬✨\n"
        "Try 'Epdi iruka?' or 'Saptiya?' to start chatting!"
    )

# ✅ Setup Telegram Bot
def main():
    """Run the Telegram bot."""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Telegram bot is running... Press Ctrl+C to stop.")
    app.run_polling()

# ✅ Run the bot
if __name__ == "__main__":
    main()
