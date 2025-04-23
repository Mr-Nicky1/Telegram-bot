
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Tu código de funciones aquí...

async def rotacion_loop():
    while True:
        print("Rotando...")
        await asyncio.sleep(60)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy tu bot.")

def main():
    application = ApplicationBuilder().token("AQUI_TU_TOKEN").build()

    application.add_handler(CommandHandler("start", start))

    asyncio.get_running_loop().create_task(rotacion_loop())

    application.run_polling()

if __name__ == "__main__":
    main()
