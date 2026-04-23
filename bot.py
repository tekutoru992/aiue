import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# -----------------------------
# 起動時
# -----------------------------
@bot.event
async def on_ready():
    print(f"ログイン完了: {bot.user}")
    await bot.tree.sync()


# -----------------------------
# /hello（動作確認）
# -----------------------------
@bot.tree.command(name="hello", description="挨拶します")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("こんにちは！")


# -----------------------------
# /ban（BAN）
# -----------------------------
@bot.tree.command(name="ban", description="ユーザーをBANします")
@app_commands.describe(member="BANするユーザー", reason="理由")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("権限がありません。", ephemeral=True)

    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member} をBANしました。")


# -----------------------------
# /unban（UNBAN）
# -----------------------------
@bot.tree.command(name="unban", description="ユーザーをUNBANします")
@app_commands.describe(username="名前#タグ の形式で入力")
async def unban(interaction: discord.Interaction, username: str):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("権限がありません。", ephemeral=True)

    banned_users = await interaction.guild.bans()
    name, discriminator = username.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (name, discriminator):
            await interaction.guild.unban(user)
            return await interaction.response.send_message(f"{user} をUNBANしました。")

    await interaction.response.send_message("そのユーザーはBANされていません。")


# -----------------------------
# ボタンUI（YouTubeリンク）
# -----------------------------
class YoutubeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="てくとるのチャンネルのURLを表示",
                url="https://www.youtube.com/@tekutoru_YT"
            )
        )


# -----------------------------
# /youtube（あなたのチャンネルを表示）
# -----------------------------
@bot.tree.command(name="youtube", description="てくとるのチャンネルを表示します")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message(
        "チャンネル登録してね！",
        view=YoutubeView()
    )


# -----------------------------
# ログ：削除
# -----------------------------
@bot.event
async def on_message_delete(message):
    log = discord.utils.get(message.guild.text_channels, name="bot-log")
    if log:
        await log.send(f"🗑️ 削除: {message.author} → {message.content}")


# -----------------------------
# ログ：編集
# -----------------------------
@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        log = discord.utils.get(before.guild.text_channels, name="bot-log")
        if log:
            await log.send(
                f"✏️ 編集: {before.author}\n"
                f"前: {before.content}\n"
                f"後: {after.content}"
            )


# -----------------------------
# Bot起動
# -----------------------------
inport os
bot.run(os.getenv("TOKEN"))
