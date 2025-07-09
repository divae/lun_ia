import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

MOON_PHASES = [
    {
        "name": "New Moon",
        "recommendation": "Ideal for new beginnings and setting intentions.",
        "ritual": "Write down your wishes for this cycle and keep them under your pillow.",
        "quote": "Every night the Moon reminds us that we can always renew ourselves."
    },
    {
        "name": "First Quarter",
        "recommendation": "Time to take action and move forward with your projects.",
        "ritual": "Make a list of concrete steps for your goals.",
        "quote": "Believe in your growth, like the Moon that grows every night."
    },
    {
        "name": "Full Moon",
        "recommendation": "Perfect for celebrating achievements and expressing gratitude.",
        "ritual": "Perform a small gratitude ritual under the Moonlight.",
        "quote": "Shine with your own light, like the Moon at its brightest."
    },
    {
        "name": "Last Quarter",
        "recommendation": "Time to let go, cleanse, and reflect.",
        "ritual": "Get rid of what you no longer need, physically or emotionally.",
        "quote": "Let go of what weighs you down, the Moon also renews itself."
    }
]

def get_moon_phase():
    """Calculate the current moon phase index (0-3)."""
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    r = year % 100
    r %= 19
    if r > 9:
        r -= 19
    phase = ((r * 11) % 30) + month + day
    if month < 3:
        phase += 2
    phase -= 8.3
    phase = int(phase + 0.5) % 30
    if phase < 7:
        return 0  # New Moon
    if phase < 15:
        return 1  # First Quarter
    if phase < 22:
        return 2  # Full Moon
    return 3      # Last Quarter

def moon(update, context):
    """Send the current moon phase, recommendation, ritual, and quote."""
    idx = get_moon_phase()
    phase = MOON_PHASES[idx]
    message = (
        f"🌙 Today is {phase['name']}.\n\n"
        f"🔬 {phase['recommendation']}\n"
        f"✨ Ritual: {phase['ritual']}\n"
        f"💬 Quote of the day: {phase['quote']}"
    )
    update.message.reply_text(message)

def start(update, context):
    """Send a welcome message and usage instructions."""
    update.message.reply_text("Hello! Use /moon to get the current moon phase, a recommendation, and a ritual.")

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set in the environment.")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('moon', moon))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main() 