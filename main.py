import discord
import os
import random
import time
import asyncio
from quart import Quart, request
from discord.ext import commands, tasks
from discord.ext.commands import MemberConverter

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
converter = MemberConverter()
bot = commands.Bot(command_prefix = '!', intents=intents)
server = client.get_guild("556557388161875975")
app = Quart(__name__)

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  print('El aleman')

@bot.command()
async def trade(ctx):
  listaDeMsg = ctx.message.content.split()
  embedInCase = discord.Embed(description="β **Error de Syntax** \n\n*Uso del comando*:\n`!trade <usuario interesado> <rol ofrecido> <rol deseado>`", color=15684176)
  inTradeable = ["π ππΌπππππππ π", "π§ββοΈ π΄π½π²π°π½ππ°π³πΎπ π§ββοΈ", "π ππππππππ π", "ππ’ππ« πΈπΈπΈ", "ππ’ππ« πΈπΈ", "ππ’ππ« πΈ", "ββ π£π₯π’ππ¨π₯πππ’π₯ ββ"]
  try:
    listaDeMsg[1], listaDeMsg[2], listaDeMsg[3]
    userInter = await converter.convert(ctx, listaDeMsg[1][2:len(listaDeMsg[1]) - 1])
    rolOfrenda = discord.utils.get(ctx.guild.roles, id=int(listaDeMsg[2][3:len(listaDeMsg[2]) - 1]))
    rolDeseado = discord.utils.get(ctx.guild.roles, id=int(listaDeMsg[3][3:len(listaDeMsg[3]) - 1]))
    if rolOfrenda.name in inTradeable:
      embedInCase = discord.Embed(description="β οΈ **Error de Argumento** \n\n*El rol* {uno.mention} *no es apto para ser intercambiado*".format(uno = rolOfrenda), color=16763402)
      await ctx.send(embed=embedInCase)
      return
    if rolDeseado.name in inTradeable:
      embedInCase = discord.Embed(description="β οΈ **Error de Argumento** \n\n*El rol* {uno.mention} *no es apto para ser intercambiado*".format(uno = rolDeseado), color=16763402)
      await ctx.send(embed=embedInCase)
      return
    if rolOfrenda not in ctx.author.roles:
      embedInCase = discord.Embed(description="β οΈ **Error de Argumento** \n\n*El rol* {0.mention} *no esta en tu posesiΓ³n*".format(rolOfrenda), color=16763402)
      await ctx.send(embed=embedInCase)
      return
    if rolDeseado not in userInter.roles:
      embedInCase = discord.Embed(description="β οΈ **Error de Argumento** \n\n*El rol* {uno.mention} *no esta en la posesiΓ³n de* {dos.mention}".format(uno = rolDeseado, dos = userInter), color=16763402)
      await ctx.send(embed=embedInCase)
      return
  except IndexError:
    await ctx.send(embed=embedInCase)
    return

  def check(reaction, user):
    if user == userInter and (str(reaction.emoji) == 'β' or str(reaction.emoji) == 'β'):
      return reaction
  def checktwo(reaction, user):
    if (user == userInter or user == ctx.author) and (str(reaction.emoji) == 'β' or str(reaction.emoji) == 'β'):
      return reaction, user
  embedInCase = discord.Embed(description='β **Esperando confirmaciΓ³n...** \n\n*Esperando a que* {0.mention} *acepte " β " o rechace " β " la peticiΓ³n*'.format(userInter), color=16743168)
  confMsg = await ctx.send(embed=embedInCase)
  await confMsg.add_reaction("β")
  await confMsg.add_reaction("β")
  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    await confMsg.edit(embed=embedInCase)
  except asyncio.TimeoutError:  
    embedInCase = discord.Embed(description='β° **PeticiΓ³n Caducada** \n\n*Se ha agotado el tiempo de espera para completar la peticiΓ³n...*', color=15684176)
    await confMsg.edit(embed=embedInCase)
    return
  if reaction.emoji == 'β':
    await confMsg.remove_reaction("β", userInter)
  if reaction.emoji == 'β':
    embedInCase = discord.Embed(description='β **PeticiΓ³n  Rechazada** \n\n*No se ha podido completar el intercambio de roles...*', color=15684176)
    await confMsg.edit(embed=embedInCase)
    return
  embedInCase = discord.Embed(description='β οΈ **ΒΏEstas seguro?** \n\n*Para completar el intercambio es necesario que los dos usuarios reaccionen con *"β" *para confirmar que:* \n\n{uno.mention} darΓ‘ {dos.mention} y obtendrΓ‘ {tres.mention} \n{cuatro.mention} darΓ‘ {tres.mention} y obtendrΓ‘ {dos.mention} \n\n*En caso de no estar de acuerdo reaccionar con* "β"'.format(uno = ctx.author, dos = rolOfrenda, tres = rolDeseado, cuatro = userInter), color=16763402)
  await confMsg.edit(embed=embedInCase)
  try:
    pepe = True
    greenVotes = 0
    lever1 = 0
    lever2 = 0
    while pepe == True:
      reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=checktwo)
      if reaction.emoji == "β":
        if user == userInter and lever1 != 1:
          greenVotes += 1
          lever1 = 1
        if user == ctx.author and lever2 != 1:
          greenVotes += 1
          lever2 = 1
      if greenVotes >= 2:
        embedInCase = discord.Embed(description='β **Intercambio Exitoso** \n\n*Β‘Se ha completado el intercambio de roles exitosamente!*', color=2883328)
        await ctx.author.remove_roles(rolOfrenda)
        await ctx.author.add_roles(rolDeseado)
        await userInter.remove_roles(rolDeseado)
        await userInter.add_roles(rolOfrenda)
        await confMsg.edit(embed=embedInCase)
        return
      if reaction.emoji == "β":
        embedInCase = discord.Embed(description='β **PeticiΓ³n  Rechazada** \n\n*No se ha completado el intercambio de roles...*', color=15684176)
        await confMsg.edit(embed=embedInCase)
        return
  except asyncio.TimeoutError:
    embedInCase = discord.Embed(description='β° **PeticiΓ³n Caducada** \n\n*Se ha agotado el tiempo de espera para completar la peticiΓ³n...*', color=15684176)
    await confMsg.edit(embed=embedInCase)
    return
@trade.error
async def info_error(ctx, error):
  embedInCase = discord.Embed(description="β **Error de Syntax** \n\n*Uso del comando*:\n`!trade <usuario interesado> <rol ofrenda> <rol deseado>`", color=15684176)
  
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

    if message.content.startswith('!jackbox') and message.channel.name == str("π₯socialπ₯"):
        await message.channel.send('https://jackbox.lol')

    if message.content.startswith("ch!loltober") and message.channel.name == str("π₯socialπ₯"):
      await message.channel.send("https://i.imgur.com/6qhd0kQ.png") 
      
    if message.content.startswith("ch!culazo") and message.channel.name == str("π₯socialπ₯"):
      await message.channel.send("https://i.imgur.com/o1RxatM.jpeg") 
    
    if message.content.startswith("ch!pat ferchini") and message.channel.name == str("π₯socialπ₯"):
      await message.channel.send("https://media.tenor.com/images/092bd440c1d335e4e250c93ecb60dd4a/tenor.gif") 

    if message.content.startswith("cuak") and message.channel.name == str("π₯socialπ₯"):
      await message.channel.send("https://i.imgur.com/71pQHvA.png") 
      
    if message.content.startswith("ch!ihop goth") and message.channel.name == str("π₯socialπ₯"):
      await message.channel.send("https://i.imgur.com/3fH16oM.png") 
    
    if str("SKU:DSDECO0006") in message.clean_content and message.author.id == 292953664492929025:
      await message.reply("<@&920856824025084024>")
    
    if str("SKU:DSDECO0005") in message.clean_content and message.author.id == 292953664492929025:
      await message.reply("<@&920856824025084024>") 
    if message.clean_content.startswith("!trade") and message.channel.name == "π±tradeoπ±":
      await bot.process_commands(message)

@app.route('/', methods=['GET'])
async def endpoint():
    return '', 200
  
@app.route('/sloots', methods=['POST'])
async def slootsHandler():
    canal = bot.get_channel(902208191276912660)
    await canal.send("*Se ha canjeado la carta* **" + request.headers["Carta"] + "** *por el usuario:* **" + request.headers["Jugador"] + "**")
    return '', 200
PORT = os.environ.get('PORT')
bot.loop.create_task(app.run_task('0.0.0.0', PORT))
bot.run(os.getenv('TOKEN'))
