import discord
from redbot.core import commands
import coinmarketcap

class Kriptocog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "87b19629-91ab-4a66-a4e7-aee344b115ac" # CoinMarketCap API anahtarını buraya girin

    @commands.command(name="kripto")
    async def get_crypto(self, ctx, count: int = 10):
        # CoinMarketCap API'ye bağlanın
        client = coinmarketcap.CoinMarketCap(self.api_key)

        # İstenen sayıda kripto para birimini alın
        data = client.ticker(limit=count)

        # Verileri mesaj olarak formatlayın
        message = f"İlk {count} kripto para birimi:\n\n"
        for currency in data:
            rank = currency['rank']
            name = currency['name']
            symbol = currency['symbol']
            price = currency['price_usd']
            message += f"{rank}. {name} ({symbol}): ${price}\n"

        # Mesajı gönderin
        await ctx.send(message)

def setup(bot):
    bot.add_cog(CryptoCog(bot))