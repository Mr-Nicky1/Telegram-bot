import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Configuración básica del log
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Lista de espera y zonas
espera = []
zona1 = []
zona2 = []
zona3 = []

# Funciones de comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de zonas. Usa /z1, /z2, /z3, /espera para comenzar.")

async def z1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    zona1.append(user)
    await update.message.reply_text(f"{user} agregado a Zona 1.")

async def z2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    zona2.append(user)
    await update.message.reply_text(f"{user} agregado a Zona 2.")

async def z3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    zona3.append(user)
    await update.message.reply_text(f"{user} agregado a Zona 3.")

async def espera_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    espera.append(user)
    await update.message.reply_text(f"{user} agregado a la lista de espera.")

# Función principal para iniciar el bot
async def main():
    # Reemplaza esto con tu token real
    TOKEN = "7582219898:AAFhKu5Tu3V7jk5J55dCc6CRNfeh4Qw8QvI"
    
    application = Application.builder().token(TOKEN).build()

    # Añadiendo los handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("z1", z1))
    application.add_handler(CommandHandler("z2", z2))
    application.add_handler(CommandHandler("z3", z3))
    application.add_handler(CommandHandler("espera", espera_cmd))

    # Ejecutar el bot
    await application.run_polling()

# Punto de entrada
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())