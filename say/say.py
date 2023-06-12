from redbot.core import commands

import discord

class Say(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command()

    async def yaz(self, ctx, *, args):

        kanal = ctx.channel  # Varsayılan olarak komutun kullanıldığı kanal

        mesaj = args  # Komutla birlikte verilen mesaj

        

        # Eğer kanal belirtilmişse

        if args.startswith("#"):

            kanal_adi, mesaj = args.split(maxsplit=1)  # İlk boşluğa kadar olan kısmı kanal adı olarak alıyoruz

            kanal_adi = kanal_adi[1:]  # "#" işaretini kaldırıyoruz

            kanal = discord.utils.get(ctx.guild.channels, name=kanal_adi)  # Kanal adına göre kanal nesnesini buluyoruz

        

        await kanal.send(mesaj)







