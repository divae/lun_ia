import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler
from datetime import datetime
import random
import json
from telegram.ext import ApplicationBuilder
import locale
from astral import LocationInfo
from astral.moon import moonrise
from telegram.ext import ConversationHandler, MessageHandler, filters

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

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

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

async def moon(update, context):
    """Send the current day in Spanish, the lunar message, and moonrise times for Madrid and Buenos Aires."""
    idx = get_moon_phase()
    phase_name = MOON_PHASE_NAMES[idx]
    phase_data = MOON_DATA[phase_name]
    days = days_until_new_moon()
    recommendation = random.choice(phase_data["recommendations"])
    ritual = random.choice(phase_data["rituals"])
    quote = random.choice(phase_data["quotes"])
    tip = random.choice(phase_data["tips"])
    now = datetime.now().strftime('%A, %-d de %B de %Y')

    # Moonrise for Madrid (hemisferio norte)
    madrid = LocationInfo("Madrid", "Spain", "Europe/Madrid", 40.4168, -3.7038)
    buenos_aires = LocationInfo("Buenos Aires", "Argentina", "America/Argentina/Buenos_Aires", -34.61, -58.38)
    today = datetime.now().date()
    try:
        moonrise_madrid = moonrise(madrid.observer, date=today)
        moonrise_madrid_str = moonrise_madrid.strftime('%H:%M') if moonrise_madrid else "No visible"
    except Exception:
        moonrise_madrid_str = "No visible"
    try:
        moonrise_ba = moonrise(buenos_aires.observer, date=today)
        moonrise_ba_str = moonrise_ba.strftime('%H:%M') if moonrise_ba else "No visible"
    except Exception:
        moonrise_ba_str = "No visible"

    message = (
        f"✨ *LUN.IA - Mensaje Lunar Diario* ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 *{now.capitalize()}*\n"
        f"🌙 *Fase lunar:* {phase_name}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔮 *Recomendación:*\n{recommendation}\n\n"
        f"🧘 *Ritual:*\n{ritual}\n\n"
        f"💬 *Cita del día:*\n_{quote}_\n\n"
        f"🗓️ *Próxima Luna Nueva:* Faltan {days} días\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 *Tip lunar:* {tip}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(message, parse_mode='Markdown')
    await update.message.reply_text("¿Te gustaría anotar algo sobre tu proyecto hoy? Usa /anotar para registrar tu avance, idea o logro.")

async def start(update, context):
    """Send a welcome message and usage instructions."""
    await update.message.reply_text("¡Hola! Usa /moon para obtener la fase lunar actual, una recomendación y un ritual.")

NOTE, = range(1)

async def ask_note(update, context):
    await update.message.reply_text(
        "¿Te gustaría anotar algo sobre tu proyecto hoy? Escribe tu avance, bloqueo, idea o logro y lo guardaré para ti.\n\nSi no quieres anotar nada, escribe /cancelar.")
    return NOTE

async def save_note(update, context):
    user_id = str(update.effective_user.id)
    note_text = update.message.text
    now = datetime.now()
    phase_idx = get_moon_phase()
    phase_name = MOON_PHASE_NAMES[phase_idx]
    note_entry = {
        "date": now.strftime('%Y-%m-%d'),
        "phase": phase_name,
        "note": note_text
    }
    # Cargar y guardar en user_notes.json
    try:
        with open("user_notes.json", "r", encoding="utf-8") as f:
            notes = json.load(f)
    except Exception:
        notes = {}
    if user_id not in notes:
        notes[user_id] = []
    notes[user_id].append(note_entry)
    with open("user_notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    await update.message.reply_text("¡Nota guardada! Puedes ver tu historial con /logros.")
    return ConversationHandler.END

async def cancel_note(update, context):
    await update.message.reply_text("Anotación cancelada.")
    return ConversationHandler.END

async def show_logros(update, context):
    user_id = str(update.effective_user.id)
    try:
        with open("user_notes.json", "r", encoding="utf-8") as f:
            notes = json.load(f)
    except Exception:
        notes = {}
    user_notes = notes.get(user_id, [])
    if not user_notes:
        await update.message.reply_text("Aún no tienes logros ni notas guardadas. Usa /anotar para registrar tu avance.")
        return
    msg = "📒 *Tu historial de notas y logros:*\n\n"
    for n in user_notes[-10:][::-1]:
        msg += f"{n['date']} ({n['phase']}):\n{n['note']}\n\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def meditacion(update, context):
    args = context.args
    tema = args[0].lower() if args else 'proyectos'
    phase_idx = get_moon_phase()
    phase_name = MOON_PHASE_NAMES[phase_idx]
    try:
        with open("rituals_db.json", "r", encoding="utf-8") as f:
            rituals_db = json.load(f)
        meditaciones = rituals_db[phase_name]["meditaciones"].get(tema, [])
    except Exception:
        meditaciones = []
    if meditaciones:
        texto = random.choice(meditaciones)
        await update.message.reply_text(f"🧘 Meditación para {tema} en {phase_name}:\n\n{texto}")
    else:
        await update.message.reply_text(f"No hay meditación registrada para el tema '{tema}' en {phase_name}.")

async def mantra(update, context):
    args = context.args
    tema = args[0].lower() if args else 'proyectos'
    phase_idx = get_moon_phase()
    phase_name = MOON_PHASE_NAMES[phase_idx]
    try:
        with open("rituals_db.json", "r", encoding="utf-8") as f:
            rituals_db = json.load(f)
        mantras = rituals_db[phase_name]["mantras"].get(tema, [])
    except Exception:
        mantras = []
    if mantras:
        texto = random.choice(mantras)
        await update.message.reply_text(f"🕉️ Mantra para {tema} en {phase_name}:\n\n" + '"' + texto + '"')
    else:
        await update.message.reply_text(f"No hay mantra registrado para el tema '{tema}' en {phase_name}.")

async def conjuro(update, context):
    args = context.args
    tema = args[0].lower() if args else 'proteccion'
    phase_idx = get_moon_phase()
    phase_name = MOON_PHASE_NAMES[phase_idx]
    try:
        with open("rituals_db.json", "r", encoding="utf-8") as f:
            rituals_db = json.load(f)
        conjuros = rituals_db[phase_name]["conjuros"].get(tema, [])
    except Exception:
        conjuros = []
    if conjuros:
        texto = random.choice(conjuros)
        await update.message.reply_text(f"🔮 Conjuro para {tema} en {phase_name}:\n\n{texto}")
    else:
        await update.message.reply_text(f"No hay conjuro registrado para el tema '{tema}' en {phase_name}.")

async def contacto(update, context):
    msg = (
        "¿Quieres una consulta personalizada, acompañamiento lunar o inspiración para tu proyecto?\n"
        "Puedes contactarme directamente en Telegram: @divae\n\n"
        "¿Te gustaría apoyar este proyecto? Invítame a un café virtual en: https://buymeacoffee.com/estela\n\n"
        "En LUN.IA combino mi experiencia personal, intuición y herramientas de inteligencia artificial para ofrecerte inspiración, rituales y guía adaptados a ti y a tu momento."
    )
    await update.message.reply_text(msg)

# Conversation handler para anotar
note_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('anotar', ask_note)],
    states={
        NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_note)]
    },
    fallbacks=[CommandHandler('cancelar', cancel_note)]
)

CHANNEL_CHAT_ID = '@lun_ia_oficial'

async def send_daily_moon_message(app):
    idx = get_moon_phase()
    phase_name = MOON_PHASE_NAMES[idx]
    phase_data = MOON_DATA[phase_name]
    days = days_until_new_moon()
    recommendation = random.choice(phase_data["recommendations"])
    ritual = random.choice(phase_data["rituals"])
    quote = random.choice(phase_data["quotes"])
    tip = random.choice(phase_data["tips"])
    now = datetime.now().strftime('%A, %-d de %B de %Y')
    message = (
        f"✨ *LUN.IA - Mensaje Lunar Diario* ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 *{now.capitalize()}*\n"
        f"🌙 *Fase lunar:* {phase_name}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔮 *Recomendación:*\n{recommendation}\n\n"
        f"🧘 *Ritual:*\n{ritual}\n\n"
        f"💬 *Cita del día:*\n_{quote}_\n\n"
        f"🗓️ *Próxima Luna Nueva:* Faltan {days} días\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 *Tip lunar:* {tip}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"¿Quieres inspiración personalizada, mantras, meditaciones o anotar tus logros?\n"
        f"Habla conmigo en privado: [@lun_ia_my_bot](https://t.me/lun_ia_my_bot)"
    )
    await app.bot.send_message(chat_id=CHANNEL_CHAT_ID, text=message, parse_mode='Markdown')

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set in the environment.")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('moon', moon))
    app.add_handler(CommandHandler('logros', show_logros))
    app.add_handler(note_conv_handler)
    app.add_handler(CommandHandler('meditacion', meditacion))
    app.add_handler(CommandHandler('mantra', mantra))
    app.add_handler(CommandHandler('conjuro', conjuro))
    app.add_handler(CommandHandler('contacto', contacto))

    import asyncio
    asyncio.run(send_daily_moon_message(app))

    app.run_polling()

if __name__ == "__main__":
    main() 