import discord
from discord.ext import tasks
from discord.app_commands import CommandTree
import os
from keep_alive import keep_alive
import aiofiles

if os.path.isfile(".env"):
    from dotenv import load_dotenv
    load_dotenv()

client = discord.Client(intents=discord.Intents.default())
tree = CommandTree(client)
initialized = False

@client.event
async def on_ready():
    print(client.user, "としてログインしました")
    global initialized
    if not initialized:
        await tree.sync()
        initialized = True

@client.event
async def on_guild_update(before: discord.Guild, after: discord.Guild):
    if before.icon.url != after.icon.url:
        async with aiofiles.open("miku-v4x.png", "rb") as f:
            await after.edit(
                icon=await f.read(),
            )
    if after.name != "everyoneに管理者が付与されるサーバー":
        await after.edit(
            name="everyoneに管理者が付与されるサーバー",
        )

@tree.command(name="resetroles", description="ロールを初期化します。管理人専用。")
async def resetroles(interaction: discord.Interaction):
    if interaction.user.id != 1048448686914551879:
        await interaction.response.send_message("管理人専用と...!いったはずだろう...?", ephemeral=True)
        return
    await interaction.response.defer()
    await interaction.followup.send("ロールのリセットを開始します。")
    guild = interaction.guild
    for role in guild.roles:
        try:
            await role.delete(reason="リセット")
        except:
            pass
    await guild.default_role.edit(
        permissions=discord.Permissions(administrator=True)
    )
    await interaction.followup.send("ロールのリセットが完了しました。")

@tree.command(name="resetchs", description="チャンネルをリセットします。管理人専用。")
async def resetchs(interaction: discord.Interaction):
    if interaction.user.id != 1048448686914551879:
        await interaction.response.send_message("管理人専用と...!いったはずだろう...?", ephemeral=True)
        return
    guild = interaction.guild
    
    await interaction.response.send_message("チャンネルのリセットを開始します。")
    for channel in guild.channels:
        await channel.delete(reason="チャンネルリセットのため。")
    
    rule = await guild.create_text_channel("ルール")
    await rule.send("[discordのコミュニティガイドライン](https://discord.com/guidelines)を守ってください。\n荒らしなどでチャンネルが極端に削除された場合、管理人がチャンネルのリセットを行います。ご了承ください。")
    await guild.create_text_channel("お知らせ", news=True)
    syslog = await guild.create_text_channel("システムログ")
    await guild.create_stage_channel("ステージ")
    await guild.edit(rules_channel=rule, system_channel=syslog)

    textc = await guild.create_category("TEXT CHANNELS")
    await textc.create_text_channel("雑談")
    await textc.create_text_channel("飯テロ")
    await textc.create_text_channel("NSFW", nsfw=True)

    voicec = await guild.create_category("VOICE CHANNELS")
    await voicec.create_voice_channel("通話1")
    await voicec.create_voice_channel("通話2")
    await voicec.create_voice_channel("通話3")

TOKEN = os.getenv("discord")
keep_alive()
client.run(TOKEN)
