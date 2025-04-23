import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

espera = []
zona1 = []
zona2 = []
zona3 = []

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¡Hola! Soy tu bot. Usa /ayuda para ver comandos.")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/z1 - Pasar a Zona 1\n"
        "/z2 - Pasar a Zona 2\n"
        "/z3 - Pasar a Zona 3\n"
        "/espera - Pasar a Espera\n"
        "/tomarlibre - Tomarse libre\n"
        "/exit - Salir de todas las listas\n"
        "/ver - Ver estado actual"
    )

async def mover_a(update: Update, destino: list, nombre: str):
    for lista in [espera, zona1, zona2, zona3]:
        if nombre in lista:
            lista.remove(nombre)
    if nombre not in destino:
        destino.append(nombre)

async def z1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    await mover_a(update, zona1, nombre)
    await update.message.reply_text(f"{nombre} pasó a Zona 1")

async def z2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    await mover_a(update, zona2, nombre)
    await update.message.reply_text(f"{nombre} pasó a Zona 2")

async def z3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    await mover_a(update, zona3, nombre)
    await update.message.reply_text(f"{nombre} pasó a Zona 3")

async def espera_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    await mover_a(update, espera, nombre)
    await update.message.reply_text(f"{nombre} fue a la espera")

async def tomarlibre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    for lista in [espera, zona1, zona2, zona3]:
        if nombre in lista:
            lista.remove(nombre)
    await update.message.reply_text(f"{nombre} se tomó libre")

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    for lista in [espera, zona1, zona2, zona3]:
        if nombre in lista:
            lista.remove(nombre)
    await update.message.reply_text(f"{nombre} salió de todas las zonas")

async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        f"Esperando: {', '.join(espera)}\n"
        f"Zona 1: {', '.join(zona1)}\n"
        f"Zona 2: {', '.join(zona2)}\n"
        f"Zona 3: {', '.join(zona3)}"
    )
    await update.message.reply_text(texto)

async def rotacion_loop():
    while True:
        if espera:
            persona = espera.pop(0)
            zona1.append(persona)
        await asyncio.sleep(120)

def main():
    app = ApplicationBuilder().token("TU_TOKEN_AQUI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("z1", z1))
    app.add_handler(CommandHandler("z2", z2))
    app.add_handler(CommandHandler("z3", z3))
    app.add_handler(CommandHandler("espera", espera_cmd))
    app.add_handler(CommandHandler("tomarlibre", tomarlibre))
    app.add_handler(CommandHandler("exit", exit))
    app.add_handler(CommandHandler("ver", ver))

    # Corrección para evitar el error del event loop
    async def run_bot():
        app.create_task(rotacion_loop())
        await app.run_polling()

    asyncio.run(run_bot())

if name == "main":
    main()