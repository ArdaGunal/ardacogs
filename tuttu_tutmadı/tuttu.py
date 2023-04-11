from redbot.core import commands
import discord


class Tuttu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.tutulan_sayi = None
        self.tutulan_kisi = None

    @commands.command()
    async def tuttu(self, ctx, channel: discord.TextChannel):
        self.players.clear()
        self.tutulan_sayi = None
        self.tutulan_kisi = None
        await ctx.send("Oyun başladı. Kanalda biri tuttu dediğinde ✅, tutmadı dediğinde ❌ reaksiyonları eklenecektir.")
        msg = await channel.send("Tutulacak sayıyı belirleyin.")
        response = await self.bot.wait_for(
            "message",
            check=lambda m: m.author == ctx.author and m.channel == channel
        )
        if response.content.isdigit():
            self.tutulan_sayi = int(response.content)
            self.tutulan_kisi = ctx.author
            await msg.edit(content=f"Tutulacak sayı **{self.tutulan_sayi}** olarak belirlendi.\n{self.tutulan_kisi.mention} tuttu.")
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
        else:
            await ctx.send("Lütfen geçerli bir sayı girin.")
            return

        def check(reaction, user):
            return user != self.bot.user and reaction.message.id == msg.id and user == self.tutulan_kisi

        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            if str(reaction.emoji) == "✅":
                self.players.append(user)
            elif str(reaction.emoji) == "❌":
                pass
            if len(self.players) >= 2:
                break

        await ctx.send(f"{self.players[0].mention} kazandı!")
        self.players.clear()
        self.tutulan_sayi = None
        self.tutulan_kisi = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.tutulan_sayi is not None and self.tutulan_kisi is not None:
            if str(self.tutulan_sayi) in message.content:
                if message.author == self.tutulan_kisi:
                    await message.add_reaction("🎉")
                else:
                    await message.add_reaction("❌")