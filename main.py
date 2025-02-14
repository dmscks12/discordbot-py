import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name="처벌공고", description="이용약관 위반 처벌 공고를 작성합니다.")
@app_commands.default_permissions(administrator=True)
async def punishment(interaction: discord.Interaction, 이름: str, 계급: str, 소속: str, 처벌사유: str, 처벌내용: str):
    embed = discord.Embed(
        title="⚖️ 커뮤니티 관리팀 - 이용약관 위반 처벌 공고",
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
    대상_정보 = f"```📋 이름: {이름}\n👤 계급: {계급}\n🏢 소속: {소속}```"
    embed.add_field(name="🎯 처벌 대상", value=대상_정보, inline=False)
    embed.add_field(name="❌ 처벌 사유", value=f"```{처벌사유}```", inline=False)
    embed.add_field(name="⚡ 처벌 내용", value=f"```{처벌내용}```", inline=False)
    embed.set_footer(text=f"공고작성자: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="차단", description="사용자를 서버에서 차단합니다.")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, 멤버: discord.Member, *, 사유: str = None):
    if interaction.user.top_role <= 멤버.top_role:
        await interaction.response.send_message("자신보다 높거나 같은 역할의 멤버를 차단할 수 없습니다.", ephemeral=True)
        return
    try:
        await 멤버.ban(reason=사유)
        embed = discord.Embed(
            description=f"👤 {멤버.mention} 님이 서버에서 차단되었습니다.",
            color=discord.Color.red()
        )
        if 사유:
            embed.add_field(name="사유", value=사유)
        embed.set_footer(text=f"처리자: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("봇의 권한이 부족하여 차단할 수 없습니다.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"차단 중 오류가 발생했습니다: {str(e)}", ephemeral=True)

@bot.tree.command(name="추방", description="사용자를 서버에서 추방합니다.")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, 멤버: discord.Member, *, 사유: str = None):
    if interaction.user.top_role <= 멤버.top_role:
        await interaction.response.send_message("자신보다 높거나 같은 역할의 멤버를 추방할 수 없습니다.", ephemeral=True)
        return
    try:
        await 멤버.kick(reason=사유)
        embed = discord.Embed(
            description=f"👤 {멤버.mention} 님이 서버에서 추방되었습니다.",
            color=discord.Color.red()
        )
        if 사유:
            embed.add_field(name="사유", value=사유)
        embed.set_footer(text=f"처리자: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("봇의 권한이 부족하여 추방할 수 없습니다.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"추방 중 오류가 발생했습니다: {str(e)}", ephemeral=True)

@bot.tree.command(name="경고", description="사용자에게 경고를 추가합니다.")
@app_commands.default_permissions(kick_members=True)
async def warn(interaction: discord.Interaction, 멤버: discord.Member, *, 경고사유: str):
    if interaction.user.top_role <= 멤버.top_role:
        await interaction.response.send_message("자신보다 높거나 같은 역할의 멤버에게 경고를 추가할 수 없습니다.", ephemeral=True)
        return

    # 실제 경고 기록을 추가하는 로직을 여기 구현해야 합니다.
    # 예시로 간단한 응답을 추가했습니다.

    try:
        embed = discord.Embed(
            title="🚨 경고 알림",
            description=f"👤 {멤버.mention} 님에게 경고가 추가되었습니다.",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="📋 경고 사유", value=f"```{경고사유}```", inline=False)
        embed.set_footer(text=f"경고 추가자: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"경고 추가 중 오류가 발생했습니다: {str(e)}", ephemeral=True)

@bot.tree.command(name="뮤트", description="사용자를 서버에서 뮤트 처리합니다.")
@app_commands.default_permissions(manage_messages=True)
async def mute(interaction: discord.Interaction, 멤버: discord.Member, 시간: str, *, 사유: str = None):
    if interaction.user.top_role <= 멤버.top_role:
        await interaction.response.send_message("자신보다 높거나 같은 역할의 멤버를 뮤트할 수 없습니다.", ephemeral=True)
        return

    # 뮤트 시간 설정 예시 (시간은 문자열로 입력받아 처리해야 함)
    # 여기서는 예시로 10분을 설정하겠습니다.
    try:
        await 멤버.add_roles(discord.utils.get(interaction.guild.roles, name="Muted"))
        embed = discord.Embed(
            description=f"👤 {멤버.mention} 님이 뮤트 처리되었습니다.",
            color=discord.Color.purple()
        )
        if 사유:
            embed.add_field(name="사유", value=사유)
        embed.set_footer(text=f"뮤트 처리자: {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("봇의 권한이 부족하여 뮤트할 수 없습니다.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"뮤트 처리 중 오류가 발생했습니다: {str(e)}", ephemeral=True)

bot.run('MTMzOTU4MjA4NDQ4NTg3MzcxNA.Gc7iJC.Unsie_ujU0pVoAQ9VkB8Omf_cleMMvZYyR5wrk')
