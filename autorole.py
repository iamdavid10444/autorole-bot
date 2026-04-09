import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MEMBER_ROLE_ID = 1491874337769132072  # Utente

@bot.event
async def on_ready():
    print(f"Bot online come {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        role = member.guild.get_role(MEMBER_ROLE_ID)

        if role is None:
            print("Ruolo non trovato")
            return

        await member.add_roles(role)
        print(f"Ruolo dato a {member.name}")

    except Exception as e:
        print(f"Errore in on_member_join: {e}")

@bot.command()
async def testrole(ctx):
    try:
        role = ctx.guild.get_role(MEMBER_ROLE_ID)

        if role is None:
            await ctx.send("❌ Ruolo non trovato.")
            return

        await ctx.author.add_roles(role)
        await ctx.send(f"✅ Ti ho dato il ruolo {role.name}")

    except Exception as e:
        await ctx.send(f"❌ Errore: {e}")
        print(f"Errore in testrole: {e}")

bot.run(os.getenv("TOKEN"))