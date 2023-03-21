import discord
from redbot.core import commands
from typing import List
from requests.exceptions import HTTPError

class CryptoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def multicoin(self, ctx: commands.Context, *coins: str) -> None:
        """
        Gets the current USD value for a list of coins
        `coins` must be a list of white space separated crypto coins
        e.g. `[p]multicoin BTC BCH LTC ETH DASH XRP`
        """
        coin_list = await self.get_coins(coins) if coins else await self.get_latest_coins()
        if not coin_list:
            await ctx.send("The provided list of coins aren't acceptable.")
            return

        if await ctx.embed_requested():
            embed = discord.Embed(title="Crypto coin comparison")
            for coin in coin_list[:25]:
                price = coin.quote["USD"].price
                msg = f"1 {coin.symbol} is {price:,.2f} USD"
                embed.add_field(name=coin.name, value=msg)
            await ctx.send(embed=embed)
        else:
            msg = ""
            for coin in coin_list[:25]:
                price = coin.quote["USD"].price
                msg += f"1 {coin.symbol} is {price:,.2f} USD\n"
            await ctx.send(msg)

    async def get_latest_coins(self) -> List:
        try:
            data = await self.bot.coinmarketcap.ticker(0, convert="USD")
            return data
        except HTTPError:
            raise commands.CommandError("Failed to fetch coin data.")

    async def get_coins(self, coins: List[str]) -> List:
        try:
            data = await self.bot.coinmarketcap.ticker(coins, convert="USD")
            return data
        except HTTPError:
            raise commands.CommandError("Failed to fetch coin data.")
