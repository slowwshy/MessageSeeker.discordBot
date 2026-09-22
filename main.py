import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
senha = os.getenv("senha")

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="sh! ", intents=intents)

def dividir_em_blocos(texto, limite=2000):
    blocos = []
    while len(texto) > limite:
        corte = texto.rfind("\n", 0, limite)
        if corte == -1:
            corte = limite
        blocos.append(texto[:corte])
        texto = texto[corte:].lstrip("\n")
    blocos.append(texto)
    return blocos

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(mensagem):
    if mensagem.author == bot.user:  # evita o bot responder a si mesmo
        return

    if mensagem.content.startswith("sh! "):
        termo = mensagem.content[4:]

        encontradas = []
        async for m in mensagem.channel.history(limit=None, oldest_first=True):
            if termo in m.content:
                encontradas.append(m)

        if not encontradas:
            await mensagem.channel.send("Não encontrei nada com esse termo.")
            return

        resposta = "\n".join(
            f"{m.jump_url}"
            for m in encontradas
        )
        texto_completo = f"Encontrei {len(encontradas)} mensagem(ns):\n{resposta}"

        for bloco in dividir_em_blocos(texto_completo):
           await mensagem.channel.send(bloco)
        

bot.run(senha)