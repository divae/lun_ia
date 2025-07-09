import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from datetime import datetime
import random
import json

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Constants for moon phase calculation
MOON_CYCLE_DAYS = 30
NEW_MOON_THRESHOLD = 7
FIRST_QUARTER_THRESHOLD = 15
FULL_MOON_THRESHOLD = 22

# Fases lunares en el mismo orden que en moon_data.json
MOON_PHASE_NAMES = ["Luna Nueva", "Cuarto Creciente", "Luna Llena", "Cuarto Menguante"]

# Cargar datos desde el archivo JSON
with open("moon_data.json", encoding="utf-8") as f:
    MOON_DATA = json.load(f)

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
    phase = ((r * 11) % MOON_CYCLE_DAYS) + month + day
    if month < 3:
        phase += 2
    phase -= 8.3
    phase = int(phase + 0.5) % MOON_CYCLE_DAYS
    if phase < NEW_MOON_THRESHOLD:
        return 0  # Luna Nueva
    if phase < FIRST_QUARTER_THRESHOLD:
        return 1  # Cuarto Creciente
    if phase < FULL_MOON_THRESHOLD:
        return 2  # Luna Llena
    return 3      # Cuarto Menguante

def days_until_new_moon():
    """Calculate days remaining until the next New Moon."""
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    r = year % 100
    r %= 19
    if r > 9:
        r -= 19
    phase = ((r * 11) % MOON_CYCLE_DAYS) + month + day
    if month < 3:
        phase += 2
    phase -= 8.3
    phase = int(phase + 0.5) % MOON_CYCLE_DAYS
    days = (MOON_CYCLE_DAYS - phase) % MOON_CYCLE_DAYS
    if days == 0:
        days = MOON_CYCLE_DAYS
    return days

def moon(update, context):
    """Send the current moon phase, random recommendation, ritual, quote, days until next New Moon, and a random tip from the database."""
    idx = get_moon_phase()
    phase_name = MOON_PHASE_NAMES[idx]
    phase_data = MOON_DATA[phase_name]
    days = days_until_new_moon()
    recommendation = random.choice(phase_data["recommendations"])
    ritual = random.choice(phase_data["rituals"])
    quote = random.choice(phase_data["quotes"])
    tip = random.choice(phase_data["tips"])
    message = (
        f"🌙 Hoy es {phase_name}.\n\n"
        f"🔬 {recommendation}\n"
        f"✨ Ritual: {ritual}\n"
        f"💬 Cita del día: {quote}\n\n"
        f"🗓️ Faltan {days} días para la próxima Luna Nueva.\n"
        f"💡 Tip lunar: {tip}"
    )
    update.message.reply_text(message)

def start(update, context):
    """Send a welcome message and usage instructions."""
    update.message.reply_text("¡Hola! Usa /moon para obtener la fase lunar actual, una recomendación y un ritual.")

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