import discord
from discord.ext import commands
import random
import os

bot_token = "MTEyMzI3NTUxMDc1MTk1MjkxOA.GSyLw0.kfCWKai4UvW_O2YQ50xynBodYL2rt_LOCTLfQA"  # Botunuzun token'ı
invite_channel_id = 1075788177626910912  # Davet loggerin çalıştığı kanalın ID'si
disney_file = "Disney.txt"  # Disney Plus hesaplarının bulunduğu dosya
netflix_folder = "Netflix"  # Netflix hesaplarının bulunduğu klasör
valorant_file = "Valorants.txt"
minecraft_file = "Minecraft.txt"
admin_role_id = 1075788060920401950  # Admin rolünün ID'si

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')  # Varsayılan yardım komutunu kaldırıyoruz

@bot.event
async def on_ready():
    print('Bot başlatıldı.')
    await bot.change_presence(activity=discord.Game(name="!yardim yazarak yardım alabilirsiniz"))

@bot.command()
async def yardim(ctx):
    help_embed = discord.Embed(title="Komut Listesi", description="Botun mevcut komutları aşağıda listelenmiştir.", color=0x00ff00)
    help_embed.add_field(name="!netflix", value="Ücretsiz Netflix hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!disney", value="Ücretsiz Disney Plus hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!valorant", value="Ücretsiz Valorant Hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!minecraft", value="Ücretsiz Minecraft Hesabı almak için kullanılır.", inline=False)
    help_embed.add_field(name="!stock", value="Hesap stok durumunu kontrol etmek için kullanılır.", inline=False)
    help_embed.add_field(name="!kacinvite", value="Davet sayılarını kontrol etmek için kullanılır.", inline=False)
    await ctx.send(embed=help_embed)

@bot.command()
async def netflix(ctx):
    account = get_account_from_folder(netflix_folder)
    if account:
        file = discord.File(account, filename="Netflix.txt")
        await ctx.author.send("İşte ücretsiz bir Netflix hesabı:", file=file)
        remove_account_from_folder(netflix_folder, account)  # Hesabı klasörden silme işlemi
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Netflix hesapları tükenmiş.")

@bot.command()
async def disney(ctx):
    account = get_account_from_file(disney_file)
    if account:
        await ctx.author.send(f"İşte ücretsiz bir Disney Plus hesabı:\n{account}")
        remove_account_from_file(disney_file, account)  # Hesabı dosyadan silme işlemi
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Disney Plus hesapları tükenmiş.")

@bot.command()
async def valorant(ctx):
    invite = get_invite_from_file(valorant_file)
    if invite:
        await ctx.author.send(f"İşte ücretsiz bir Valorant hesap:\n{invite}")
        remove_invite_from_file(valorant_file, invite)
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Valorant hesapları tükenmiş.")

@bot.command()
async def minecraft(ctx):
    invite = get_invite_from_file(minecraft_file)
    if invite:
        await ctx.author.send(f"İşte ücretsiz bir Minecraft Hesabı :\n{invite}")
        remove_invite_from_file(minecraft_file, invite)
        await ctx.send("Hesabınız DM'den gönderildi.")
    else:
        await ctx.send("Üzgünüm, Minecraft Hesapları tükenmiş.")

@bot.command()
async def stock(ctx):
    stock_embed = discord.Embed(title="Hesap Stok Durumu", description="Mevcut hesap stok durumu aşağıda listelenmiştir.", color=0x00ff00)
    stock_embed.add_field(name="Netflix", value=f"Toplam {count_files_in_folder(netflix_folder)} adet hesap bulunuyor.")
    stock_embed.add_field(name="Disney Plus", value=f"Toplam {count_lines_in_file(disney_file)} adet hesap bulunuyor.")
    stock_embed.add_field(name="Valorant Hesaplar", value=f"Toplam {count_lines_in_file(valorant_file)} adet Hesap bulunuyor.")
    stock_embed.add_field(name="Minecraft Hesaplar", value=f"Toplam {count_lines_in_file(minecraft_file)} adet Hesapbulunuyor.")
    await ctx.send(embed=stock_embed)

@bot.command()
async def kacinvite(ctx):
    invite = await ctx.guild.invites()
    for inv in invite:
        if inv.inviter == ctx.author:
            invite_count = inv.uses
            break
    else:
        invite_count = 0

    invite_embed = discord.Embed(title="Davet Sayısı", description=f"{ctx.author} kullanıcısının davet sayısı: {invite_count}", color=0x00ff00)
    await ctx.send(embed=invite_embed)

def get_account_from_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    files = os.listdir(folder_path)
    if files:
        account_file = random.choice(files)
        account_path = os.path.join(folder_path, account_file)
        return account_path
    return None

def remove_account_from_folder(folder_name, account_path):
    os.remove(account_path)

def get_account_from_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        accounts = file.readlines()
        if accounts:
            account = random.choice(accounts)
            return account.strip()
    return None

def remove_account_from_file(file_name, account):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        accounts = file.readlines()
    with open(file_path, "w") as file:
        for acc in accounts:
            if acc.strip() != account:
                file.write(acc)

def get_invite_from_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        invites = file.readlines()
        if invites:
            invite = random.choice(invites)
            return invite.strip()
    return None

def remove_invite_from_file(file_name, invite):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        invites = file.readlines()
    with open(file_path, "w") as file:
        for inv in invites:
            if inv.strip() != invite:
                file.write(inv)

def count_files_in_folder(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    files = os.listdir(folder_path)
    return len(files)

def count_lines_in_file(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, "r") as file:
        lines = file.readlines()
        return len(lines)

bot.run(bot_token)
