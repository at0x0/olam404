import discord
import os
import random
import time
import asyncio
import flask
from flask import Flask, request
from threading import Thread
from discord.ext import commands
from discord.ext.commands import MemberConverter

app = Flask('')
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
converter = MemberConverter()
bot = commands.Bot(command_prefix = '!', intents=intents)
server = client.get_guild("556557388161875975")
loop = asyncio.get_event_loop()

@app.route('/')
def home():
    return "olap estoy vivo"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def slootsHandler(user):
  canal = bot.get_channel(id=852689298368364544)
  await canal.send(user)
  
@app.route("/sloots", methods=["PUT"])
def api():
  data = request.headers.get("pepe")
  if data is None:
    return {"type": "Error", "content": "No data requested"}
  else:
    loop.run_until_complete(slootsHandler(data))
    return {"type": "Error", "content": "Data specified does not exist"}
  
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  print('El aleman')

@bot.command()
async def trade(ctx):
  listaDeMsg = ctx.message.content.split()
  embedInCase = discord.Embed(description="❌ **Error de Syntax** \n\n*Uso del comando*:\n`!trade <usuario interesado> <rol ofrecido> <rol deseado>`", color=15684176)
  inTradeable = ["🎂 𝙋𝘼𝙎𝙏𝙀𝙇𝙊𝙎𝙊 🎂", "🧙‍♂️ 𝙴𝙽𝙲𝙰𝙽𝚃𝙰𝙳𝙾𝚁 🧙‍♂️", "🎇 𝐋𝐔𝐌𝐈𝐍𝐀𝐑𝐘 🎇", "𝐓𝐢𝐞𝐫 🅸🅸🅸", "𝐓𝐢𝐞𝐫 🅸🅸", "𝐓𝐢𝐞𝐫 🅸", "▀▄ 𝗣𝗥𝗢𝗖𝗨𝗥𝗔𝗗𝗢𝗥 ▄▀"]
  try:
    listaDeMsg[1], listaDeMsg[2], listaDeMsg[3]
    userInter = await converter.convert(ctx, listaDeMsg[1][2:len(listaDeMsg[1]) - 1])
    rolOfrenda = discord.utils.get(ctx.guild.roles, id=int(listaDeMsg[2][3:len(listaDeMsg[2]) - 1]))
    rolDeseado = discord.utils.get(ctx.guild.roles, id=int(listaDeMsg[3][3:len(listaDeMsg[3]) - 1]))
    if rolOfrenda.name in inTradeable:
      embedInCase = discord.Embed(description="⚠️ **Error de Argumento** \n\n*El rol* {uno.mention} *no es apto para ser intercambiado*".format(uno = rolOfrenda), color=16763402)
      await ctx.send(embed=embedInCase)
      return
    if rolDeseado.name in inTradeable:
      embedInCase = discord.Embed(description="⚠️ **Error de Argumento** \n\n*El rol* {uno.mention} *no es apto para ser intercambiado*".format(uno = rolDeseado), color=16763402)
      await ctx.send(embed=embedInCase)
      return
    if rolOfrenda not in ctx.author.roles:
      embedInCase = discord.Embed(description="⚠️ **Error de Argumento** \n\n*El rol* {0.mention} *no esta en tu posesión*".format(rolOfrenda), color=16763402)
      await ctx.send(embed=embedInCase)
      return
    if rolDeseado not in userInter.roles:
      embedInCase = discord.Embed(description="⚠️ **Error de Argumento** \n\n*El rol* {uno.mention} *no esta en la posesión de* {dos.mention}".format(uno = rolDeseado, dos = userInter), color=16763402)
      await ctx.send(embed=embedInCase)
      return
  except IndexError:
    await ctx.send(embed=embedInCase)
    return

  def check(reaction, user):
    if (user == userInter and str(reaction.emoji) == '✅') or (user == userInter and str(reaction.emoji) == '❌'):
      return reaction
  embedInCase = discord.Embed(description='⌛ **Esperando confirmación...** \n\n*Esperando a que* {0.mention} *acepte " ✅ " o rechace " ❌ " la petición*'.format(userInter), color=16743168)
  confMsg = await ctx.send(embed=embedInCase)
  await confMsg.add_reaction("✅")
  await confMsg.add_reaction("❌")
  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    await confMsg.edit(embed=embedInCase)
  except asyncio.TimeoutError:
    embedInCase = discord.Embed(description='⏰ **Petición Caducada** \n\n*Se ha agotado el tiempo de espera para completar la petición...*', color=15684176)
    await confMsg.edit(embed=embedInCase)
    return
  if reaction.emoji == '✅':
    embedInCase = discord.Embed(description='✅ **Intercambio Exitoso** \n\n*¡Se ha completado el intercambio de roles exitosamente!*', color=2883328)
    await ctx.author.remove_roles(rolOfrenda)
    await ctx.author.add_roles(rolDeseado)
    await userInter.remove_roles(rolDeseado)
    await userInter.add_roles(rolOfrenda)
    await confMsg.edit(embed=embedInCase)
    return
  if reaction.emoji == '❌':
    embedInCase = discord.Embed(description='❌ **Petición  Rechazada** \n\n*No se ha podido completar el intercambio de roles...*', color=15684176)
    await confMsg.edit(embed=embedInCase)
    return
@trade.error
async def info_error(ctx, error):
  embedInCase = discord.Embed(description="❌ **Error de Syntax** \n\n*Uso del comando*:\n`!trade <usuario interesado> <rol ofrenda> <rol deseado>`", color=15684176)
  
  if isinstance(error, commands.MemberNotFound):
    await ctx.send(embed=embedInCase)
    return
  if isinstance(error, commands.CommandInvokeError):
    await ctx.send(embed=embedInCase)
    return

@bot.event
async def on_message(message):

    if message.author == client.user:
        return
    if str("@olam404") in message.clean_content:
        time.sleep(0.5)
        await message.reply('no ande pingeando zorra')
        await message.channel.send("<:ragecat:830156708822122566>") 

    if message.content.startswith('!jackbox') and message.channel.name == str("👥social👥"):
        await message.channel.send('https://jackbox.lol')

    if message.content.startswith("ch!loltober") and message.channel.name == str("👥social👥"):
      await message.channel.send("https://i.imgur.com/6qhd0kQ.png") 
      
    if message.content.startswith("ch!culazo") and message.channel.name == str("👥social👥"):
      await message.channel.send("https://i.imgur.com/o1RxatM.jpeg") 
    
    if message.content.startswith("ch!pat ferchini") and message.channel.name == str("👥social👥"):
      await message.channel.send("https://media.tenor.com/images/092bd440c1d335e4e250c93ecb60dd4a/tenor.gif") 

    if message.content.startswith("cuak") and message.channel.name == str("👥social👥"):
      await message.channel.send("https://i.imgur.com/71pQHvA.png") 
      
    if message.content.startswith("ch!ihop goth") and message.channel.name == str("👥social👥"):
      await message.channel.send("https://i.imgur.com/3fH16oM.png") 
    
    if str("SKU:DSDECO0006") in message.clean_content and message.author.id == 292953664492929025:
      await message.reply("<@&920856824025084024>")
    
    if str("SKU:DSDECO0005") in message.clean_content and message.author.id == 292953664492929025:
      await message.reply("<@&920856824025084024>") 
    if message.clean_content.startswith("!trade") and message.channel.name == "💱tradeo💱":
      await bot.process_commands(message)
keep_alive()
bot.run(os.getenv('TOKEN'))