import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

MEMBER_ROLE_ID = 1460660733036597412  # 

@bot.event
async def on_ready():
    print(f"Bot online come {bot.user}")

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(MEMBER_ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f"Ruolo dato a {member.name}")
    else:
        print("Ruolo non trovato")

import os
bot.run(os.getenv("TOKEN"))