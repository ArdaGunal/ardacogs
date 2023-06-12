from redbot.core import commands

import discord

class Say(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command()

    async def yaz(self, ctx, *, args):

        if args.startswith("<#") and ">" in args:

            kanal_id, mesaj = args.split(maxsplit=1)

            kanal_id = kanal_id[2:-1]

            kanal = discord.utils.get(ctx.guild.channels, id=int(kanal_id))

            if kanal:

                await kanal.send(mesaj)

            else:

                await ctx.send("Belirtilen kanal bulunamadı.")

        else:

            await ctx.send(args)

        

        await ctx.message.delete()

def setup(bot):

    bot.add_cog(Say(bot))




   






