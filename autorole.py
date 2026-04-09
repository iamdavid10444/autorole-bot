import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

MEMBER_ROLE_ID = 1491874337769132072  # Utente

ROSSO_ROLE_ID = 1491874337761001490
ARANCIONE_ROLE_ID = 1491874337761001489
GIALLO_ROLE_ID = 1491874337761001488
VERDE_ROLE_ID = 1491874337761001487
BLU_ROLE_ID = 1491874337761001486
VIOLA_ROLE_ID = 1491874337761001485
MARRONE_ROLE_ID = 1491874337761001484
NERO_ROLE_ID = 1491874337761001483
BIANCO_ROLE_ID = 1491874337761001482

NORD_ROLE_ID = 1491874337328857217
CENTRO_ROLE_ID = 1491874337328857216
SUD_ROLE_ID = 1491874337328857215

MASCHIO_ROLE_ID = 1491874337328857214
NON_BINARIO_ROLE_ID = 1491874337328857212
FEMMINA_ROLE_ID = 1491874337328857213

COLOR_ROLE_IDS = [
    ROSSO_ROLE_ID,
    ARANCIONE_ROLE_ID,
    GIALLO_ROLE_ID,
    VERDE_ROLE_ID,
    BLU_ROLE_ID,
    VIOLA_ROLE_ID,
    MARRONE_ROLE_ID,
    NERO_ROLE_ID,
    BIANCO_ROLE_ID,
]

GENERE_ROLE_IDS = [
    MASCHIO_ROLE_ID,
    NON_BINARIO_ROLE_ID,
    FEMMINA_ROLE_ID,
]

REACTION_ROLES = {
    "🔴": ROSSO_ROLE_ID,
    "🟠": ARANCIONE_ROLE_ID,
    "🟡": GIALLO_ROLE_ID,
    "🟢": VERDE_ROLE_ID,
    "🔵": BLU_ROLE_ID,
    "🟣": VIOLA_ROLE_ID,
    "🟤": MARRONE_ROLE_ID,
    "⚫": NERO_ROLE_ID,
    "⚪": BIANCO_ROLE_ID,
    "⬆️": NORD_ROLE_ID,
    "➡️": CENTRO_ROLE_ID,
    "⬇️": SUD_ROLE_ID,
    "♂️": MASCHIO_ROLE_ID,
    "⚧️": NON_BINARIO_ROLE_ID,
    "♀️": FEMMINA_ROLE_ID,
}

REACTION_MESSAGE_ID = None

@bot.event
async def on_ready():
    print(f"Bot online come {bot.user}")

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(MEMBER_ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f"Ruolo Utente dato a {member.name}")
    else:
        print("Ruolo Utente non trovato")

@bot.command()
@commands.has_permissions(administrator=True)
async def setuproles(ctx):
    global REACTION_MESSAGE_ID

    text = (
        "✨ **SCEGLI I TUOI RUOLI** ✨\n\n"
        "**🎨 COLORI**\n"
        "🔴 Rosso\n"
        "🟠 Arancione\n"
        "🟡 Giallo\n"
        "🟢 Verde\n"
        "🔵 Blu\n"
        "🟣 Viola\n"
        "🟤 Marrone\n"
        "⚫ Nero\n"
        "⚪ Bianco\n\n"
        "**🌍 ZONA**\n"
        "⬆️ Nord\n"
        "➡️ Centro\n"
        "⬇️ Sud\n\n"
        "**👤 INFO**\n"
        "♂️ Maschio\n"
        "⚧️ Non binario\n"
        "♀️ Femmina\n\n"
        "📌 Clicca sulle emoji qui sotto per ottenere i ruoli."
    )

    msg = await ctx.send(text)
    REACTION_MESSAGE_ID = msg.id

    for emoji in REACTION_ROLES:
        await msg.add_reaction(emoji)

    await ctx.send("Pannello ruoli creato.")

async def remove_roles_from_group(member, group_ids):
    roles_to_remove = [role for role in member.roles if role.id in group_ids]
    if roles_to_remove:
        await member.remove_roles(*roles_to_remove)

@bot.event
async def on_raw_reaction_add(payload):
    global REACTION_MESSAGE_ID

    if payload.user_id == bot.user.id:
        return
    if REACTION_MESSAGE_ID is None:
        return
    if payload.message_id != REACTION_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = str(payload.emoji)
    role_id = REACTION_ROLES.get(emoji)
    if role_id is None:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    if role_id in COLOR_ROLE_IDS:
        await remove_roles_from_group(member, COLOR_ROLE_IDS)

    if role_id in GENERE_ROLE_IDS:
        await remove_roles_from_group(member, GENERE_ROLE_IDS)

    await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    global REACTION_MESSAGE_ID

    if REACTION_MESSAGE_ID is None:
        return
    if payload.message_id != REACTION_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = str(payload.emoji)
    role_id = REACTION_ROLES.get(emoji)
    if role_id is None:
        return

    role = guild.get_role(role_id)
    if role is None:
        return

    await member.remove_roles(role)

bot.run(os.getenv("TOKEN"))