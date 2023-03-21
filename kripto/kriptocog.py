import discord
from discord.ext import commands
import coinmarketcap

class kriptocog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "f18323d7-1cb4-4ce5-8872-d93b25104900" # CoinMarketCap API anahtarını buraya girin

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