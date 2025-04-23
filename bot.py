import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
import asyncio

# Tu token de bot
TOKEN = "7582219898:AAFhKu5Tu3V7jk5J55dCc6CRNfeh4Qw8QvI"

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Lista de espera y zonas
espera = []
zonas = {"z1": None, "z2": None, "z3": None}

# Comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bot activo y funcionando!")

async def z1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await manejar_zona(update, "z1")

async def z2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await manejar_zona(update, "z2")

async def z3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await manejar_zona(update, "z3")

async def manejar_zona(update: Update, zona):
    user = update.message.from_user.first_name
    if zonas[zona] is None:
        zonas[zona] = user
        await update.message.reply_text(f"{user} ahora está en {zona.upper()}")
    else:
        if user not in espera:
            espera.append(user)
            await update.message.reply_text(f"{user}, agregado a la lista de espera.")

async def espera_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if espera:
        await update.message.reply_text("Lista de espera:\n" + "\n".join(espera))
    else:
        await update.message.reply_text("La lista de espera está vacía.")

async def exit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    for zona, ocupado in zonas.items():
        if ocupado == user:
            zonas[zona] = None
            await update.message.reply_text(f"{user} salió de {zona.upper()}")
            await rotar_usuarios()
            return
    if user in espera:
        espera.remove(user)
        await update.message.reply_text(f"{user} eliminado de la lista de espera.")

async def rotar_usuarios():
    for zona in zonas:
        if zonas[zona] is None and espera:
            siguiente = espera.pop(0)
            zonas[zona] = siguiente

# Función principal
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("z1", z1))
    app.add_handler(CommandHandler("z2", z2))
    app.add_handler(CommandHandler("z3", z3))
    app.add_handler(CommandHandler("espera", espera_cmd))
    app.add_handler(CommandHandler("exit", exit_cmd))

    await app.run_polling()

if name == "main":
    asyncio.run(main())