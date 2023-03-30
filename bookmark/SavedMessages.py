# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class savedMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.saved_messages = {}

    @commands.command(name="save")
    async def save_message(self, ctx, message: discord.Message):
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅"

        await ctx.send("Mesajı kaydetmek istediğinizden emin misiniz? ✅ tepkisine basın.")

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except:
            await ctx.send("Zaman aşımı! Mesaj kaydedilmedi.")
        else:
            if ctx.guild.id in self.saved_messages:
                self.saved_messages[ctx.guild.id] += [message.content]
            else:
                self.saved_messages[ctx.guild.id] = [message.content]
            user_saved_messages = [f"{i+1}. {saved_message}" for i, saved_message in enumerate(self.saved_messages.get(ctx.guild.id))]
            await ctx.send(f"Mesaj kaydedildi! Kişisel listeniz: \n" + "\n".join(user_saved_messages))

    @commands.command(name="list")
    async def list_saved_messages(self, ctx):
        user_saved_messages = [f"{i+1}. {saved_message}" for i, saved_message in enumerate(self.saved_messages.get(ctx.guild.id, []))]
        await ctx.send("Kaydedilmiş mesajlarınız: \n" + "\n".join(user_saved_messages))

    @commands.command(name="delete")
    async def delete_saved_message(self, ctx, message_index: int):
        if ctx.guild.id in self.saved_messages and message_index <= len(self.saved_messages[ctx.guild.id]):
            del self.saved_messages[ctx.guild.id][message_index-1]
            user_saved_messages = [f"{i+1}. {saved_message}" for i, saved_message in enumerate(self.saved_messages.get(ctx.guild.id, []))]
            await ctx.send("Mesaj silindi! Güncel liste: \n" + "\n".join(user_saved_messages))
        else:
            await ctx.send("Geçersiz mesaj numarası!")