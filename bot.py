import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# Variables globales
zona_1 = []
zona_2 = []
zona_3 = []
espera = []

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Usa los comandos para unirte a una zona o a la lista de espera.")

# Comando /z1
async def z1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    if user not in zona_1:
        zona_1.append(user)
        await update.message.reply_text(f"{user} añadido a Zona 1.")
    else:
        await update.message.reply_text(f"{user}, ya estás en Zona 1.")

# Comando /z2
async def z2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    if user not in zona_2:
        zona_2.append(user)
        await update.message.reply_text(f"{user} añadido a Zona 2.")
    else:
        await update.message.reply_text(f"{user}, ya estás en Zona 2.")

# Comando /z3
async def z3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    if user not in zona_3:
        zona_3.append(user)
        await update.message.reply_text(f"{user} añadido a Zona 3.")
    else:
        await update.message.reply_text(f"{user}, ya estás en Zona 3.")

# Comando /espera
async def lista_espera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    if user not in espera:
        espera.append(user)
        await update.message.reply_text(f"{user} añadido a la lista de espera.")
    else:
        await update.message.reply_text(f"{user}, ya estás en la lista de espera.")

# Comando /exit
async def salir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    for lista in [zona_1, zona_2, zona_3, espera]:
        if user in lista:
            lista.remove(user)
    await update.message.reply_text(f"{user} ha salido de todas las listas.")

# Comando /tomarlibre
async def tomar_libre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if espera:
        siguiente = espera.pop(0)
        await update.message.reply_text(f"{siguiente}, ahora puedes tomar el lugar libre.")
    else:
        await update.message.reply_text("No hay nadie en la lista de espera.")

if _name_ == "_main_":
    TOKEN = os.environ.get("TELEGRAM_TOKEN")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("z1", z1))
    application.add_handler(CommandHandler("z2", z2))
    application.add_handler(CommandHandler("z3", z3))
    application.add_handler(CommandHandler("espera", lista_espera))
    application.add_handler(CommandHandler("exit", salir))
    application.add_handler(CommandHandler("tomarlibre", tomar_libre))

    application.run_polling()