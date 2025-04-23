import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Zonas y lista de espera
zonas = {"Zona 1": None, "Zona 2": None, "Zona 3": None}
espera = []
bot_activo = True
ultima_rotacion = datetime.now()
intervalo_rotacion = timedelta(minutes=120)

horarios = {
    "Colombia": ("14:16", "16:16"),
    "México": ("13:16", "15:31"),
    "Venezuela": ("15:16", "17:31"),
    "Argentina/Chile": ("16:16", "18:31"),
    "España": ("21:16", "23:31")
}

def generar_lista():
    now = datetime.now()
    tiempo_restante = max((ultima_rotacion + intervalo_rotacion - now).seconds // 60, 0)
    msg = "🕐 *Lista de Espera y Zonas Actuales*\n\n"
    for pais, (inicio, fin) in horarios.items():
        msg += f"📍 *Hora {pais}*: ⏰ {inicio} — {fin}\n"
    msg += "\n"
    for zona, user in zonas.items():
        estado = user if user else "Libre"
        msg += f"🔷 {zona}: {estado}\n"
    msg += f"\n⏳ *Rotación en {tiempo_restante} minutos*\n"
    if espera:
        msg += "\n⏱️ *En espera:* ⏱️\n" + "\n".join(espera)
    else:
        msg += "\n⏱️ *En espera:* No hay usuarios\n"
    return msg

async def enviar_lista(context):
    chat_id = context.job.chat_id
    await context.bot.send_message(chat_id=chat_id, text=generar_lista(), parse_mode=ParseMode.MARKDOWN)

async def rotar(context=None):
    global ultima_rotacion
    if not bot_activo:
        return
    zonas_copy = zonas.copy()
    if zonas_copy["Zona 3"]:
        espera.append(zonas_copy["Zona 3"])
    zonas["Zona 3"] = zonas_copy["Zona 2"]
    zonas["Zona 2"] = zonas_copy["Zona 1"]
    zonas["Zona 1"] = espera.pop(0) if espera else None
    ultima_rotacion = datetime.now()
    if context:
        await enviar_lista(context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy el bot de lista de espera. Usa /lista para ver el estado actual.")

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generar_lista(), parse_mode=ParseMode.MARKDOWN)

async def reglas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reglas_txt = """
📌 *Reglas del grupo*:
- Respeta los turnos y a los demás usuarios.
- Usa los comandos correctamente.
- No hacer spam ni abusar de los comandos.
"""
    await update.message.reply_text(reglas_txt, parse_mode=ParseMode.MARKDOWN)

async def cerrarlista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_activo
    bot_activo = False
    await update.message.reply_text("❌ La lista ha sido cerrada. Los comandos ahora están deshabilitados.")

async def abrirlista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_activo, ultima_rotacion
    bot_activo = True
    ultima_rotacion = datetime.now()
    await update.message.reply_text("✅ La lista ha sido activada. Todos los comandos están disponibles.")

async def comando_zona(update: Update, context: ContextTypes.DEFAULT_TYPE, zona):
    if not bot_activo:
        return
    user = context.args[0] if context.args else update.effective_user.mention_html()
    zonas[zona] = user
    await update.message.reply_html(f"{user} ha sido asignado a {zona}.")
    await update.message.reply_text(generar_lista(), parse_mode=ParseMode.MARKDOWN)

async def salir_zona(update: Update, context: ContextTypes.DEFAULT_TYPE, zona):
    if not bot_activo:
        return
    zonas[zona] = None
    await update.message.reply_text(f"{zona} ahora está LIBRE.")
    await update.message.reply_text(generar_lista(), parse_mode=ParseMode.MARKDOWN)

async def esperar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_activo:
        return
    user = context.args[0] if context.args else update.effective_user.mention_html()
    if user not in espera:
        espera.append(user)
        await update.message.reply_html(f"{user} ha sido añadido a la lista de espera.")
    else:
        await update.message.reply_html(f"{user} ya está en la lista de espera.")
    await update.message.reply_text(generar_lista(), parse_mode=ParseMode.MARKDOWN)

async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_activo:
        return
    user = context.args[0] if context.args else update.effective_user.mention_html()
    for zona in zonas:
        if zonas[zona] == user:
            zonas[zona] = None
    if user in espera:
        espera.remove(user)
    await update.message.reply_html(f"{user} ha sido eliminado de todas las zonas y de la lista de espera.")
    await update.message.reply_text(generar_lista(), parse_mode=ParseMode.MARKDOWN)

async def tomarlibre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_activo:
        return
    user = context.args[0] if context.args else update.effective_user.mention_html()
    for zona in zonas:
        if zonas[zona] is None:
            zonas[zona] = user
            await update.message.reply_html(f"{user} ha tomado {zona}.")
            await update.message.reply_text(generar_lista(), parse_mode=ParseMode.MARKDOWN)
            return
    await update.message.reply_html("No hay zonas libres en este momento.")

async def rotar_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_activo:
        return
    await rotar(context)

if __name__ == '__main__':
    app = ApplicationBuilder().token("TU_TOKEN_AQUI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(CommandHandler("reglas", reglas))
    app.add_handler(CommandHandler("cerrarlista", cerrarlista))
    app.add_handler(CommandHandler("abrirlista", abrirlista))
    app.add_handler(CommandHandler("z1", lambda u, c: comando_zona(u, c, "Zona 1")))
    app.add_handler(CommandHandler("z2", lambda u, c: comando_zona(u, c, "Zona 2")))
    app.add_handler(CommandHandler("z3", lambda u, c: comando_zona(u, c, "Zona 3")))
    app.add_handler(CommandHandler("exitz1", lambda u, c: salir_zona(u, c, "Zona 1")))
    app.add_handler(CommandHandler("exitz2", lambda u, c: salir_zona(u, c, "Zona 2")))
    app.add_handler(CommandHandler("exitz3", lambda u, c: salir_zona(u, c, "Zona 3")))
    app.add_handler(CommandHandler("espera", esperar))
    app.add_handler(CommandHandler("exit", exit_command))
    app.add_handler(CommandHandler("tomarlibre", tomarlibre))
    app.add_handler(CommandHandler("rotar", rotar_comando))

    async def rotacion_loop():
        while True:
            await asyncio.sleep(60)
            if bot_activo and datetime.now() >= ultima_rotacion + intervalo_rotacion:
                await rotar()

    app.create_task(rotacion_loop())
    app.run_polling()
