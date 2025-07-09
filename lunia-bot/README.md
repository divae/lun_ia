# LUN.IA Telegram Bot

A Telegram bot that provides information about the current moon phase, recommendations, rituals, quotes, and lunar tips, all in Spanish. The bot is designed for wellness, science, and lunar enthusiasts.

## Features
- Get the current moon phase in Spanish
- Receive a random recommendation, ritual, quote, and tip for the phase
- Calculates days until the next New Moon
- All content is easily editable via a JSON database
- **NEW:** Register your daily project notes and track your progress and achievements
- **NEW:** Get personalized meditations, mantras, and spells for each lunar phase and topic

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/divae/lun_ia.git
   cd lunia-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Telegram bot token**
   - Create a file called `.env` in the `lunia-bot` directory:
     ```
     TELEGRAM_TOKEN=your_token_here
     ```
   - **Never share your real token or commit `.env` to GitHub!**
   - You can use `.env.example` as a template.

4. **Run the bot**
   ```bash
   python bot.py
   ```

5. **Try it on Telegram**
   - Open your bot in Telegram and send `/moon` to get the lunar info.
   - After each lunar message, the bot will invite you to write a note about your project or day.
   - Use `/anotar` to register a new note at any time.
   - Use `/logros` to see your last 10 notes and achievements.
   - Use `/meditacion [tema]`, `/mantra [tema]` o `/conjuro [tema]` para recibir inspiración personalizada.

## Project Structure

```
lunia-bot/
├── bot.py           # Main bot code
├── moon_data.json   # Database of recommendations, rituals, quotes, and tips
├── rituals_db.json  # Meditations, mantras, and spells by lunar phase and topic
├── user_notes.json  # User notes and achievements (auto-generated)
├── requirements.txt # Python dependencies
├── .env             # Your secret token (never commit this!)
├── .env.example     # Example environment file
├── README.md        # This documentation
```

## Personal Notes & Achievements
- After each lunar message, the bot invites you to write a note about your project, progress, ideas, or feelings.
- Use `/anotar` to add a note at any time. You can cancel with `/cancelar`.
- All notes are saved in `user_notes.json` (private, not shared).
- Use `/logros` to see your last 10 notes, with date and lunar phase.
- This feature helps you reflect, track your growth, and celebrate your journey.

## Meditations, Mantras & Spells
- Use `/meditacion [tema]` to receive a meditation adapted to the current lunar phase and your chosen topic (e.g., proyectos, amor, creatividad).
- Use `/mantra [tema]` to receive a mantra for the day and your topic.
- Use `/conjuro [tema]` to receive a simple, safe spell for your intention.
- If you don't specify a topic, the bot will use a default (e.g., proyectos o protección).
- Example:
  - `/meditacion proyectos`
  - `/mantra amor`
  - `/conjuro abundancia`
- The bot will answer with a text from its curated database, adapted to the current lunar phase.

## Security: Keeping Your Token Safe
- Your Telegram token must be stored in `.env` and **never** committed to GitHub.
- `.env` is included in `.gitignore` by default.
- Share `.env.example` for collaborators to know the required variable.

## Customizing Content
- Edit `moon_data.json` to add or change recommendations, rituals, quotes, and tips for each lunar phase.
- Edit `rituals_db.json` to add or change meditations, mantras, and spells for each phase and topic.
- No need to modify the code for content updates!

## Troubleshooting
- **Bot says `TELEGRAM_TOKEN is not set in the environment.`**
  - Make sure `.env` exists in the `lunia-bot` directory and is formatted as `TELEGRAM_TOKEN=your_token_here`.
  - Run the bot from the `lunia-bot` directory.
- **FileNotFoundError for `moon_data.json` or `rituals_db.json`**
  - Ensure both files are in the same directory as `bot.py`.
- **No response in Telegram**
  - Check that your bot is running and that the token is correct.

## FAQ
**Q: Can I add more tips, meditations, mantras or spells?**  
A: Yes! Just edit the JSON files and restart the bot.

**Q: How do I keep my token secret?**  
A: Never share your `.env` file. Use `.env.example` for documentation.

**Q: Can I run this on a server?**  
A: Yes, just make sure Python and the dependencies are installed, and the `.env` file is present.

## Contributing
- Fork the repo and submit a pull request.
- Suggestions, bug reports, and improvements are welcome!

## License
MIT 