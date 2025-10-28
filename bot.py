import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
app = Application.builder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Бот запущен! Для получения инструкции введите команду: /help\n")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Доступные команды:\n"
        "/start - запустить бота\n"
        "/ping - проверить связь\n"
        "/about - информация о данном боте\n"
        "/time - текущее дата/время\n"
        "/timer <раунд> <секунд> - запустить таймер\n\n"
        "Пример: /timer 2 120 10 - 2 раунда по 120 секунд, отдых между раундами 10 секунд\n"
    )
    await update.message.reply_text(text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong ")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Boxing Timer Bot. Команды: /start, /help, /time, /timer. Автор: Виталий.")

async def time_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"Текущее время: {now}")

async def timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) not in (2, 3):
        await update.message.reply_text("Формат: /timer <раунды> <секунд_в_раунде> [отдых]\nНапример: /timer 3 30")
        return
    try:
        rounds = int(context.args[0])
        seconds = int(context.args[1])
        rest = int(context.args[2]) if len (context.args) == 3 else 0
        assert rounds > 0 and seconds > 0 and rest >= 0          
        
            
    except Exception:
        await update.message.reply_text("Введи три положительных числа. Пример: /timer 3 30 10")
        return

    for r in range(rounds, 0, -1):
        await update.message.reply_text(f"Раунд {r} начинается!")
        

        msg = await update.message.reply_text(f"Осталось {seconds} секунд")
        for t in range(seconds - 1, -1, -1):
            await asyncio.sleep(1)
            await msg.edit_text(f"Осталось {t} секунд")

        await update.message.reply_text(f"Раунд {r} завершён")

        if r > 1 and rest > 0:
                rest_msg = await update.message.reply_text(f"Отдых {rest} секунд")
                for t in range(rest - 1, -1, -1):
                    await asyncio.sleep(1)
                    await rest_msg.edit_text(f"Отдых {t} секунд")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"Все раунды завершены. Время: {now}")

 
    

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("timer", timer))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("time", time_now))
if __name__ == "__main__":
    app.run_polling()

