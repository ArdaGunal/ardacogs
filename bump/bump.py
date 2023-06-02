import discord
from redbot.core import commands, tasks
import time

class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bump_reminders = {}
        self.check_bump.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "/bump":
            channel_id = message.channel.id
            self.bump_reminders[channel_id] = time.time() + 2 * 60 * 60

    @tasks.loop(seconds=60)
    async def check_bump(self):
        for channel_id, reminder_time in list(self.bump_reminders.items()):
            if reminder_time <= time.time():
                channel = self.bot.get_channel(channel_id)
                await channel.send("2 saat geçti, lütfen tekrar /bump yazın!")
                del self.bump_reminders[channel_id]

    @check_bump.before_loop
    async def before_check_bump(self):
        await self.bot.wait_until_ready()

