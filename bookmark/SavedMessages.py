class savedMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.saved_messages = {}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "✅" and not payload.member.bot:
            message_id = payload.message_id
            user_id = payload.user_id
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(message_id)
            if channel.guild.id in self.saved_messages:
                self.saved_messages[channel.guild.id] += [(message.content, user_id)]
            else:
                self.saved_messages[channel.guild.id] = [(message.content, user_id)]

    @commands.command(name="list")
    async def list_saved_messages(self, ctx):
        user_saved_messages = [f"{i+1}. {saved_message[0]}" for i, saved_message in enumerate(self.saved_messages.get(ctx.guild.id, []) if saved_message[1] == ctx.author.id)]
        if user_saved_messages:
            await ctx.send("Kaydedilmiş mesajlarınız: \n" + "\n".join(user_saved_messages))
        else:
            await ctx.send("Kaydedilmiş mesajınız yok.")

    @commands.command(name="delete")
    async def delete_saved_message(self, ctx, message_index: int):
        user_saved_messages = self.saved_messages.get(ctx.guild.id, [])
        for i, saved_message in enumerate(user_saved_messages):
            if i == message_index - 1 and saved_message[1] == ctx.author.id:
                del user_saved_messages[i]
                await ctx.send(f"Mesaj silindi! Güncel liste: \n{self.format_user_saved_messages(user_saved_messages)}")
                return
        await ctx.send("Geçersiz mesaj numarası!")

    def format_user_saved_messages(self, saved_messages):
        return "\n".join([f"{i+1}. {saved_message[0]}" for i, saved_message in enumerate(saved_messages) if saved_message[1] == ctx.author.id])