class dbot():
	def __init__(self, info):
		import os
		try:
			import discord
			from discord.ext import commands
		except:
			print("Нет модуля discord, начинаем установку!")
			os.system("pip install discord")
		try:
			import asyncio
		except:
			print("Нет модуля asyncio, начинаем установку!")
			os.system("pip install asyncio")
		import discord
		from discord.ext import commands
		self._prefix=info["prefix"]
		self._token=info["token"]
		try:
			self._self=info["self"]=="true"
		except:
			self._self=False
		self._codes={}
		self._codes["commands"]={}
		self._client=commands.Bot(command_prefix=self._prefix, intents=discord.Intents.all())
		self._client.remove_command(help)

	def command(self, info):
		self._codes["commands"][info["name"]]={}
		code=[]
		for n in info:
			if not n in ["name","prefix"]:
				code.append(info[n])
		self._codes["commands"][info["name"]]["name"]=info["name"]
		self._codes["commands"][info["name"]]["code"]=code
		try:
			self._codes["commands"][info["name"]]["prefix"]=info["prefix"]
		except:
			self._codes["commands"][info["name"]]["prefix"]=self._prefix
	def start(self):
		_start(self._client, self)

def _start(client, info):
	
	@client.event
	async def on_ready():
		print("Бот онлайн!")
	
	@client.event
	async def on_message(message):
		if not message.author.bot:
			def remember(text):
				global command
				command = text
				return True
			if any(message.content.startswith(info._codes["commands"][cmd]["prefix"]+info._codes["commands"][cmd]["name"]) and remember(cmd) for cmd in info._codes["commands"]):
				await use([message, command, "commands"],info)
	
	if info._self:
		client.run(info._token, bot=False)
	else:
		client.run(info._token)

async def use(need, info):
	import discord
	binstr = ""
	emb = [False, discord.Embed()]
	functions = ["$title[","$description["]
	lines = info._codes[need[2]][need[1]]["code"]
	for line in lines:
		reline = line
		if any(line.startswith(func) for func in functions):
			if line.endswith("]"):
				if line.startswith("$title["):
					emb[0]=True
					emb[1].title=line[len("$title["):][:-1]
				elif line.startswith("$description["):
					emb[0]=True
					emb[1].description=line[len("$description["):][:-1]
			else:
				await need[0].channel.send(f"❌Ошибка синтаксиса на строке {lines.index(reline)+1} в `{reline}`")
		else:
			if binstr == "":
				binstr += reline
			else:
				binstr += "\n"+reline
	if emb[0]:
		await need[0].channel.send(embed=emb[1])
	else:
		await need[0].channel.send(binstr)