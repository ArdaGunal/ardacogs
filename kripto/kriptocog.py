import discord
from discord.ext import commands
from typing import Union
from coinmarketcapapi import CoinMarketCapAPI
from prettytable import PrettyTable

class CoinMarketCap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "YOUR_API_KEY" # CoinMarketCap API anahtarını buraya yazın.
        self.client = CoinMarketCapAPI(self.api_key)

    @commands.command()
    async def multicoin(self, ctx, *coins: str):
        """Shows the latest data of one or multiple cryptocurrencies"""

        if not coins:
            # Eğer herhangi bir coin verilmediyse, en popüler 10 coini listele.
            data = await self.client.cryptocurrency_listings_latest(limit=10)
            coins = [coin["symbol"] for coin in data["data"]]
        else:
            # Verilen coinleri listele.
            data = await self.get_coins(coins)

        table = self.generate_table(data)
        await ctx.send(f"```{table}```")

    async def get_coins(self, coins: Union[list, tuple]) -> list:
        """Gets the latest data of the specified cryptocurrencies"""

        data = await self.client.cryptocurrency_quotes_latest(symbol=",".join(coins), convert="USD")
        return [data["data"][coin] for coin in coins]

    def generate_table(self, data: list) -> str:
        """Generates a pretty table of the cryptocurrency data"""

        table = PrettyTable()
        table.field_names = ["Name", "Symbol", "Price", "Market Cap", "Volume", "Change (24h)"]

        for coin in data:
            name = coin["name"]
            symbol = coin["symbol"]
            price = "$" + f'{coin["quote"]["USD"]["price"]:.2f}'
            market_cap = "$" + f'{coin["quote"]["USD"]["market_cap"]:,}'
            volume = "$" + f'{coin["quote"]["USD"]["volume_24h"]:,}'
            change = f'{coin["quote"]["USD"]["percent_change_24h"]:.2f}%'

            table.add_row([name, symbol, price, market_cap, volume, change])

        return str(table)

def setup(bot):
    bot.add_cog(CoinMarketCap(bot))
