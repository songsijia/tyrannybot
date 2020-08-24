# bot.py
import os, time, json, urllib.request, pickle, discord
from dotenv import load_dotenv

# 1
from discord.ext import tasks, commands
from discord.utils import get 


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD'))
BATPHONE_CHANNEL = int(os.getenv('DISCORD_BATPHONE_CHANNEL'))
BATPHONE_ROLE = int(os.getenv('DISCORD_BATPHONE_ROLE'))

# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	send_politics.start()
	print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="ping")
async def ping(ctx):
	response = "Ping!"
	await ctx.send(response)
	
	
# batphone options below

lastread = 0

@tasks.loop(seconds=10)
async def send_politics():
	with urllib.request.urlopen("https://api.lusternia.com/news/politics.json?page=100000") as url:
		data = json.loads(url.read().decode())
		
	post = data["news"][0]
	sendstr = get_politics(post)
	if sendstr:
		channel = bot.get_channel(BATPHONE_CHANNEL)
		guild = discord.utils.get(bot.guilds, id=GUILD_ID)
		role = discord.utils.get(guild.roles,id = BATPHONE_ROLE)
		await channel.send(sendstr+role.mention)
	


def get_politics(post):
	global lastread
	print(lastread)
	print(post["id"])
	if post["id"] <= lastread:
		return False
	timesince = time.time()-post["date"]
	if timesince > 600:
		lastread = post["id"]
		return False
		
	isevent = False
	str = False
	for x in events:
		print(x[0])
		if x[0] in post["subject"]:
			isevent = True
			eventtype = x[1] 
	
	if isevent:
		lastread = post["id"]
		timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(post["date"]))
		eventstr = ""
		if eventtype == "revolt":
			eventstr = "Revolt! "
		str = "```"+eventstr+post["subject"]+" ("+timestr+")```"
	
	return str

events = {("Aether Flares Around","flares"),
	("Rikenfriez Blizzard!","revolt"),
	("Dairuchi Celebrations","revolt"),
	("The Mountain Wars and the Undervault Struggles","revolt"),
	("Hemp Wars","revolt"),
	("Orc-Furrikin Wars","revolt"),
	("Aslaran-Krokani Feud","revolt"),
	("Political Upheaval","revolt"),}

	
bot.run(TOKEN)

